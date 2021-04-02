from django.urls import re_path

from . import views

app_name = 'publications'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^(?P<slug>[-\w]+)$', views.PublicationDetail.as_view(), name='publication'),
    #re_path(r'^(?P<slug>[-\w]+)/download$', views.download_pdf, name='download_pdf'),
    
]