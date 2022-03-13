from django.urls import re_path, path

from . import views

app_name = 'profile'

urlpatterns = [
    re_path(r'^(?P<username>[0-9]{6,8})/$', views.profile, name='profile'),
    path('add_experience', views.add_experience, name='add_experience'),
]
