from django.conf.urls import url

from . import views

app_name = 'profile'

urlpatterns = [
<<<<<<< HEAD
    url(r'^(?P<username>[\w.@+-]+)/$', views.index),
=======
    url(r'(?P<username>[\w.@+-]+)/$', views.index, name='index'),
>>>>>>> 9405bf14dda453968793948f7cacebfc466f1580
]