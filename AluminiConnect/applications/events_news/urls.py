from django.conf.urls import url

from . import views

app_name = 'events_news'

urlpatterns = [
    url(r'(?P<id>[0-9])/$', views.event, name='event'),
    url(r'^$', views.index, name='index'),
]