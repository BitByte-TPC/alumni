from django.conf.urls import url

from . import views

app_name = 'news'

urlpatterns = [
    url(r'^(?P<id>[0-9])/$', views.news, name='news'),
    url(r'^$', views.index, name='index'),
]