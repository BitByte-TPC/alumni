from django.urls import path, re_path

from . import views

app_name = 'gallery'

urlpatterns = [
    # re_path(r'^event/(?P<id>[0-9])/$', views.event, name='event'),
    path('', views.gallery, name='gallery'),
    re_path(r'^(?P<slug>[-\w]+)$', views.AlbumDetail.as_view(), name='album'),

]
