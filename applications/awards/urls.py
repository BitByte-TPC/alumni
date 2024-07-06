from django.urls import path, re_path
from . import views

app_name = 'awards'

urlpatterns = [
    re_path(r'^(?P<id>\d+)/$', views.award, name='award'),
    path('', views.index, name='index'),
]