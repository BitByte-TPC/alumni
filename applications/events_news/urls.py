from django.urls import path, re_path

from . import views

app_name = 'events_news'

urlpatterns = [
    re_path(r'^event/(?P<id>[0-9]+)/$', views.event, name='event'),
    path('', views.events, name='events'),
]
