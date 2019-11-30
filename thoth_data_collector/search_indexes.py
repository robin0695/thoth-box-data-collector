from thoth_data_collector.models import PaperItem
from haystack import indexes
import datetime

class PaperItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr="created_date")

    def get_model(self):
        return PaperItem
    
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created_date__lte=datetime.datetime.now())