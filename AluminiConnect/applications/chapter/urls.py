from django.conf.urls import url

from . import views

app_name = 'chapter'

urlpatterns = [
    # url(r'^event/(?P<id>[0-9])/$', views.event, name='event'),
    url(r'^(?P<id>[0-9])/$', views.chapter, name='chapter'),
    url(r'^images/$', views.chapter_images, name='chapter_images'),
    url(r'^$', views.index, name='index')
]