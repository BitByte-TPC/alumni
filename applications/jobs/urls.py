from django.urls import path, re_path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.add_opportunity, name='add_opportunity'),
    path('filter/', views.filter, name='filter'),
    re_path(r'^del/(?P<i_id>[0-9]+)/$', views.delete_job, name='delete_job'),
]
