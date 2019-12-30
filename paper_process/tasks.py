from __future__ import absolute_import, unicode_literals

import sys
import os
from celery import shared_task
from thoth_data_collector.models import PaperItem
from urllib.request import urlopen
import shutil
from django.conf import settings
import time
import random
import logging
import subprocess
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

logger = logging.getLogger(__name__)

@shared_task
def process_paper():
    """
    process the paper based on the query from PaperItem with is_processed == 0
    actions:
        download paper
        transform paper to html
        extract text from paper

    the processed files are saved in MEDIA_URL/pdfs
    """
    data_folder = os.path.join(settings.MEDIA_ROOT, 'pdfs')
    timeout_secs = 10 # after this many seconds we give up the paper
    papers = PaperItem.objects.filter(is_processed=0)
    for paper in papers:
        paper_link = paper.paper_link + ".pdf"
        paper_id = paper.paper_link.split("/")[-1]
        paper_folder = os.path.join(data_folder, paper_id)
        output_paper_file = os.path.join(paper_folder, paper_id + ".pdf")
       
        try:
            if not os.path.exists(output_paper_file):
                # download the pdf
                req = urlopen(paper_link, None, timeout_secs)
                
                if not os.path.exists(paper_folder):
                    os.makedirs(paper_folder)

                with open(output_paper_file, "wb") as fp:
                    shutil.copyfileobj(req, fp)
                
                pdf2html.delay(output_paper_file)
                pdf2text.delay(output_paper_file)
                time.sleep(0.05 + random.unifom(0, 0.1))
            
            paper.is_processed = 1
            paper.save()
        except Exception as e:
            logger.error(e)

@shared_task
def paper_process_pipeline(paper_link, dest_dir=None):
    if not paper_link.endswith("pdf"):
        paper_link += ".pdf"
    
    if dest_dir is None:
        dest_dir = "./"
    
    timeout_secs = 10
    out_paper_name = paper_link.split("/")[-1]
    out_paper_name = os.path.join(dest_dir, out_paper_name)

    try:
        # download paper
        req = urlopen(paper_link, None, timeout_secs)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
                
        with open(out_paper_name, "wb") as fp:
            shutil.copyfileobj(req, fp)

        # transform to html
        pdf2html(out_paper_name, dest_dir)

        # transform to text
        pdf2text(out_paper_name, dest_dir)

    except Exception as e:
        logger.error(e)


@shared_task
def pdf2html(paper_file, dest_dir=None):
    if not shutil.which('pdf2htmlEX'):
        raise Exception('Error: pdf2htmlEX not exist. Pleaase install pdf2htmlEX in first.')
    if dest_dir is None:
        dest_dir = os.path.dirname(paper_file)
    basename = os.path.basename(paper_file).rsplit(".", 1)[0]

    command = "pdf2htmlEX --dest-dir %s --zoom 1.5 %s"  % (dest_dir, paper_file)
    logger.info(command)
    try:
        subprocess.call(command, shell=True)
    except Exception as e:
        logger.error(e)

@shared_task
def pdf2text(pdf_file, dest_dir=None):
    if not shutil.which('pdftotext'):
        raise Exception('Error: pdftotext not exist. Please install pdftotext in first.')
    
    basename = os.path.basename(pdf_file)
    text_basename = basename.rsplit(".", 1)[0] + ".txt"
    if dest_dir is None:
        dest_dir = os.path.dirname(pdf_file)

    text_file = os.path.join(dest_dir, text_basename)

    command = "pdftotext %s %s" % (pdf_file, text_file)
    logger.info(command)

    try:
        subprocess.call(command, shell=True)
    except Exception as e:
        logger.error(e)
