from django.conf.urls import url

from . import views

app_name = 'publications'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<slug>[-\w]+)$', views.PublicationDetail.as_view(), name='publication'),
    #url(r'^(?P<slug>[-\w]+)/download$', views.download_pdf, name='download_pdf'),
    
]