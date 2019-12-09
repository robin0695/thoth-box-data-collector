"""thoth-data-collector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from thoth_data_collector import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'papers', views.PaperViewSet)
router.register(r'paper_authors', views.PaperAuthorViewSet)
router.register(r'issue_infos', views.IssueViewSet)
router.register(r'paper/search', views.PaperSearchView, base_name='paper-search')


urlpatterns = [
    path(r'admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^papers(?P<is_recommanded>.+)/$', views.RecommandPaperList.as_view()),
    #url(r"paper_like/(?P<id>\d+)/(?P<value>-?\d)/", views.paper_like, name="paper_like")
]

