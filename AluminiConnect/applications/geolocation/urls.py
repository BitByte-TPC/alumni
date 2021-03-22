from django.conf.urls import url

from . import views

app_name = 'geolocation'

urlpatterns = [
    url(r'^update/$', views.updatePoints, name='updatePoints'),
    url(r'^$', views.index, name='index')
]