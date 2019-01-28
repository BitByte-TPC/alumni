from django.conf.urls import url

from . import views

app_name = 'events_news'

urlpatterns = [
    url(r'^event/(?P<id>[0-9])/$', views.event, name='event'),
    url(r'^$', views.events, name='events'),
]