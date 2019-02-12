from django.conf.urls import url, include

from . import views

app_name = 'members'

extrapatterns = [
    
    url(r'^(?P<programme>[.a-zA-Z]+)/(?P<branch>[A-Z]+)/$', views.branch, name="branch"),
    url(r'^$', views.batch, name="batch"),
]
urlpatterns = [
    url(r'^(?P<year>[0-9]{4})/', include(extrapatterns)),
    url(r'^sacbody/$', views.sacbody, name="sacbody"),
    url(r'^$', views.index, name='index'),
]