from django.urls import path

from . import views

app_name = 'adminportal'

urlpatterns = [
    path('', views.index, name='index'),
    path('registrations', views.registrations_index, name='registrations'),
    path('mailservice', views.mailservice_index, name='mailservice'),
]

