from django.urls import re_path

from . import views

app_name = 'geolocation'

urlpatterns = [
    re_path(r'^update/$', views.updatePoints, name='updatePoints'),
    re_path(r'^$', views.index, name='index')
]