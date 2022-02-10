from django.urls import re_path

from . import views

app_name = 'profile'

urlpatterns = [
    re_path(r'^(?P<username>[0-9A-Za-z]{6,8})/$', views.profile, name='profile'),
]
