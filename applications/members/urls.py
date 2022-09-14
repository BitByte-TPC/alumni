from django.urls import include, path, re_path

from . import views

app_name = 'members'

extrapatterns = [

    re_path(r'^(?P<programme>[.a-zA-Z]+)/(?P<branch>[A-Z]+)/$', views.branch, name="branch"),
    path('', views.batch, name="batch"),
]
urlpatterns = [
    re_path(r'^(?P<year>[0-9]{4})/', include(extrapatterns)),
    # old link
    # path('sacbody/', views.sacbody, name="sacbody"),
    # new link
    path('alumnibody/', views.alumnibody, name="alumnibody"),
    path('search/', views.search, name='search'),
    path('autosearch/', views.autoSearch, name='autosearch'),
    path('mapsearch/', views.mapSearch, name='mapsearch'),
    path('', views.index, name='index'),
]
