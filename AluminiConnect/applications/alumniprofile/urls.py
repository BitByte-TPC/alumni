from django.conf.urls import url

from . import views

app_name = 'profile'

urlpatterns = [
    url(r'^(?P<username>[0-9]{7})/$', views.profile, name='profile'),
]