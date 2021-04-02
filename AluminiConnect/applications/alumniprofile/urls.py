from django.urls import re_path

from . import views

app_name = 'profile'

urlpatterns = [
    re_path(r'^(?P<username>[0-9]{7})/$', views.profile, name='profile'),
    re_path(r'^(?P<username>[0-9]{6})/$', views.profile, name='profile'),
]