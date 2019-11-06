from django.db import models
from datetime import datetime, date


class IssueInfo(models.Model):
    issue_title = models.CharField(max_length=1000)
    issue_date = models.DateTimeField(default=datetime.now())
    issue_sn = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=datetime.now())
    created_by = models.CharField(max_length=200, default='')
    update_date = models.DateTimeField(default=datetime.now())
    update_by = models.CharField(max_length=200, default='')
    is_deleted = models.BooleanField(default=False)


# Create your models here.
class PaperItem(models.Model):
    paper_id = models.CharField(max_length=450)
    paper_title = models.CharField(max_length=4000)
    paper_link = models.CharField(max_length=3000)
    page_comments = models.CharField(max_length=300)
    is_recommanded = models.BooleanField(default=False)
    recommand_reason = models.TextField(default='')
    recommand_by = models.CharField(max_length=200, default='')
    created_date = models.DateTimeField(default=datetime.now())
    created_by = models.CharField(max_length=200, default='')
    update_date = models.DateTimeField(default=datetime.now())
    update_by = models.CharField(max_length=200, default='')
    is_processed = models.BooleanField(default=False)
    issue_info = models.ForeignKey(IssueInfo, related_name='papers', on_delete=models.CASCADE, null=True)


class PaperAuthor(models.Model):
    author_name = models.CharField(max_length=200)
    author_home_page = models.CharField(max_length=4000)
    author_email_addr = models.CharField(max_length=200)
    paper_item = models.ForeignKey(PaperItem, related_name='authors', on_delete=models.CASCADE)


class PaperCategory(models.Model):
    term = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)
    paper_item = models.ForeignKey(PaperItem, related_name='categories', on_delete=models.CASCADE)
