from django.conf.urls import url

from . import views

app_name = 'profile'

urlpatterns = [
    url(r'(?P<username>[\w.@+-]+)/$', views.index, name='profile'),
]