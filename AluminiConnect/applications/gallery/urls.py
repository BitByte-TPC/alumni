from django.urls import re_path

from . import views

app_name = 'gallery'

urlpatterns = [
    #re_path(r'^event/(?P<id>[0-9])/$', views.event, name='event'),
    re_path(r'^$', views.gallery, name='gallery'),
    re_path(r'^(?P<slug>[-\w]+)$', views.AlbumDetail.as_view(), name='album'),
    
]