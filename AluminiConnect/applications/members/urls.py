from django.urls import re_path, include

from . import views

app_name = 'members'

extrapatterns = [
    
    re_path(r'^(?P<programme>[.a-zA-Z]+)/(?P<branch>[A-Z]+)/$', views.branch, name="branch"),
    re_path(r'^$', views.batch, name="batch"),
]
urlpatterns = [
    re_path(r'^(?P<year>[0-9]{4})/', include(extrapatterns)),
    re_path(r'^sacbody/$', views.sacbody, name="sacbody"),
    re_path(r'^search/$', views.search, name='search'),
    re_path(r'^autosearch/$', views.autoSearch, name='autosearch'),
    re_path(r'^mapsearch/$', views.mapSearch, name='mapsearch'),
    re_path(r'^$', views.index, name='index'),
]