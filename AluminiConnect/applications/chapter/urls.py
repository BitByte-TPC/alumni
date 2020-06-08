from django.conf.urls import url

from . import views

app_name = 'chapter'

urlpatterns = [
    url(r'^(?P<id>[0-9])/$', views.chapter_redirect, name='chapter_redirect'),
    url(r'^images/$', views.chapter_images, name='chapter_images'),
    url(r'^r/(?P<id>[0-9])/$', views.chapter, name='chapter'),
    url(r'^$', views.index, name='index')
]