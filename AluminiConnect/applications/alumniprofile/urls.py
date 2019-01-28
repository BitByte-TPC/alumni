from django.conf.urls import url

from . import views

app_name = 'profile'

urlpatterns = [
    url(r'list/(?P<year>[0-9]{4})/$', views.index_year),
    url(r'list/', views.index),
    url(r'(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
]