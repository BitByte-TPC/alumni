from django.urls import path, re_path

from . import views

app_name = 'blog'

urlpatterns = [
    re_path(r'^(?P<id>[0-9])/$', views.blog, name='blog'),
    path('', views.index, name='index'),
]
