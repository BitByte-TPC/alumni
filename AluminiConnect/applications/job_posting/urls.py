from django.conf.urls import url

from . import views

app_name = 'jobs'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^post/', views.new_post, name='new_post'),
    url(r'^filter/', views.filter, name='filter'),
]
