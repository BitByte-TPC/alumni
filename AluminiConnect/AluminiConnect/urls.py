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
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from os import listdir
from .  import views


favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
urlpatterns = []

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^$', views.index, name='home'),
    url(r'^admin/', admin.site.urls),    
    url(r'^login/', views.LoginFormView.as_view(), name='login'),
    #url(r'^account/reset_password', views.ResetPasswordRequestView.as_view(), name="reset_password"),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^newregister/', views.new_register, name='new_register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^confirm/$', TemplateView.as_view(template_name='AluminiConnect/confirm_email.html'), name = 'confirm'),
    url(r'^success/$', TemplateView.as_view(template_name='AluminiConnect/account_success.html'), name = 'success'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^profileedit/(?P<id>[0-9]+)/$', views.profileedit, name='profileedit'),
    url(r'^profile/', include('applications.alumniprofile.urls')),
    url(r'^members/', include('applications.members.urls')),
    url(r'^events/', include('applications.events_news.urls')),
    url(r'^news/', include('applications.news.urls')),
    url(r'^newsletter/', include('applications.publications.urls')),
    url(r'^geolocation/', include('applications.geolocation.urls')),
    url(r'^alumnibody/', views.alumniBody),
    url(r'^alumnicard/', views.alumniCard, name='alumnicard'),
    url(r'^gallery/', include('applications.gallery.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^awards/', include('applications.awards.urls')),
    url(r'favicon.ico', favicon_view)
    #url(r'^', views.index, name='home'),
]

if settings.DEBUG:
    

    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
admin.site.site_header = "IIITDMJ Alumni Association"
admin.site.site_title = "Alumni Association"
admin.site.index_title = "Alumni Association Admin"
