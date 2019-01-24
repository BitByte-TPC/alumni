from django.conf.urls import url

from . import views

app_name = 'events_news'

urlpatterns = [

    url(r'^$', views.index, name='index'),
]