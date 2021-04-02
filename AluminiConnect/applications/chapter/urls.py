from django.urls import re_path

from . import views

app_name = 'chapter'

urlpatterns = [
    re_path(r'^(?P<id>[0-9])/$', views.chapter_redirect, name='chapter_redirect'),
    re_path(r'^images/$', views.chapter_images, name='chapter_images'),
    re_path(r'^r/(?P<id>[0-9])/$', views.chapter, name='chapter'),
    re_path(r'^$', views.index, name='index')
]