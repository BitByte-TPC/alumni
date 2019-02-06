from django.conf.urls import url
from . import views

app_name = 'awards'

urlpatterns = [
    url(r'^(?P<id>[0-9])/$', views.award, name='award'),
    url(r'^$', views.index, name='index'),
    
]