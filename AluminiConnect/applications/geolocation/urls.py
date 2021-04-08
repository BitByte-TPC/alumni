from django.urls import path

from . import views

app_name = 'geolocation'

urlpatterns = [
    path('update/', views.updatePoints, name='updatePoints'),
    path('', views.index, name='index')
]
