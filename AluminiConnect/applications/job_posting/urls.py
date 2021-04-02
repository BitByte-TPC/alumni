from django.urls import re_path

from . import views

app_name = 'jobs'

urlpatterns = [

    re_path(r'^$', views.index, name='index'),
]