from django.urls import re_path, path

from . import views

app_name = 'profile'

urlpatterns = [
    re_path(r'^(?P<username>[a-zA-Z0-9]{5,9})/$', views.profile, name='profile'),
    path('add_experience', views.add_experience, name='add_experience'),
    path('add_education', views.add_education, name='add_education'),
]
