from django.urls import path, re_path

from . import views

app_name = 'chapter'

urlpatterns = [
    re_path(r'^(?P<id>[0-9])/$', views.chapter_redirect, name='chapter_redirect'),
    path('images/', views.chapter_images, name='chapter_images'),
    re_path(r'^r/(?P<id>[0-9])/$', views.chapter, name='chapter'),
    path('', views.index, name='index')
]
