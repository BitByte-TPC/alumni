from django.urls import re_path
from . import views

app_name = 'awards'

urlpatterns = [
    re_path(r'^(?P<id>[0-9])/$', views.award, name='award'),
    re_path(r'^$', views.index, name='index'),
    
]