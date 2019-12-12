from django.conf.urls import url

from . import views

app_name = 'gallery'

urlpatterns = [
    #url(r'^event/(?P<id>[0-9])/$', views.event, name='event'),
    url(r'^$', views.gallery, name='gallery'),
    url(r'^(?P<slug>[-\w]+)$', views.AlbumDetail.as_view(), name='album'),
    
]