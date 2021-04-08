from django.urls import path, re_path

from . import views

app_name = 'news'

urlpatterns = [
    re_path(r'^(?P<id>[0-9])/$', views.news, name='news'),
    path('', views.index, name='index'),
]
