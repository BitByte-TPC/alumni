from django.conf.urls import url

from . import views

app_name = 'profile'

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
]