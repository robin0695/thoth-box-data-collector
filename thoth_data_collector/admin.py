from django.contrib import admin
from thoth_data_collector.models import PaperItem, IssueInfo, PaperAuthor

# Register your models here.
admin.site.register(PaperItem)
admin.site.register(IssueInfo)
admin.site.register(PaperAuthor)
