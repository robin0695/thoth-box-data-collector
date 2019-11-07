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

logger = logging.getLogger(__name__)

@shared_task
def add(x, y):
    return x+y

@shared_task
def download_paper():
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
                time.sleep(0.05 + random.unifomr(0, 0.1))
            
            paper.is_processed = 1
            paper.save()
        except Exception as e:
            logger.error(e)

@shared_task
def pdf2html(paper_file):
    dest_dir = os.path.dirname(paper_file)
    basename = os.path.basename(paper_file).split(".")[0]
    html_file = os.path.join(dest_dir, basename + ".html")
    if os.path.exists(html_file):
        return

    command = "pdf2htmlEX --dest-dir %s %s"  % (dest_dir, paper_file)
    logger.info(command)
    try:
        subprocess.call(command, shell=True)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    pass

