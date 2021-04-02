from django.urls import re_path

from . import views

app_name = 'news'

urlpatterns = [
    re_path(r'^(?P<id>[0-9])/$', views.news, name='news'),
    re_path(r'^$', views.index, name='index'),
]