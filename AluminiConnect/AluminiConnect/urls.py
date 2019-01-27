"""AluminiConnect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from os import listdir
from .  import views

urlpatterns = []

#for app in listdir('applications'):
#    urlpatterns.append(url(r'^'+app+'/', include('applications.' + app + '.urls')))

urlpatterns += [
    url(r'^admin/', admin.site.urls),    
    url(r'^login/', views.auth),
    url(r'^logout/$', auth_views.logout),
<<<<<<< HEAD
    url(r'^profile/', include('applications.alumniprofile.urls')),
=======
    url(r'profile/', include('applications.alumniprofile.urls')),
>>>>>>> 9405bf14dda453968793948f7cacebfc466f1580
    url(r'^', views.index),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
    
