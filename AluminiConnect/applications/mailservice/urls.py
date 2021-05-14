from django.urls import path

from . import views

app_name = 'mailservice'

urlpatterns = [
    path('', views.index, name='index'),
    path('email_sent/', views.email_sent, name='email_sent'),
]

