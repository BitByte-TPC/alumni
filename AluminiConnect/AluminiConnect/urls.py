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
from django.urls import include, re_path
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
    re_path(r'^$', views.index, name='home'),
    re_path(r'^admin/', admin.site.urls),    
    re_path(r'^login/$', views.LoginFormView.as_view(), name='login'),
    #re_path(r'^account/reset_password', views.ResetPasswordRequestView.as_view(), name="reset_password"),
    re_path(r'^logout/$', auth_views.logout, name='logout'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^newregister/$', views.new_register, name='new_register'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    re_path(r'^confirm/$', TemplateView.as_view(template_name='AluminiConnect/confirm_email.html'), name = 'confirm'),
    re_path(r'^success/$', TemplateView.as_view(template_name='AluminiConnect/account_success.html'), name = 'success'),
    re_path('^', include('django.contrib.auth.urls')),
    re_path(r'^password/$', views.change_password, name='change_password'),
    re_path(r'^profileedit/(?P<id>[0-9]+)/$', views.profileedit, name='profileedit'),
    re_path(r'^profile/', include('applications.alumniprofile.urls')),
    re_path(r'^members/', include('applications.members.urls')),
    re_path(r'^events/', include('applications.events_news.urls')),
    re_path(r'^news/', include('applications.news.urls')),
    re_path(r'^newsletter/', include('applications.publications.urls')),
    re_path(r'^geolocation/', include('applications.geolocation.urls')),
    re_path(r'^alumnibody/$', views.alumniBody),
    re_path(r'^alumnicard/$', views.alumniCard, name='alumnicard'),
    re_path(r'^gallery/', include('applications.gallery.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^awards/', include('applications.awards.urls')),
    re_path(r'^chapter/', include('applications.chapter.urls')),
    re_path(r'favicon.ico', favicon_view)
    #re_path(r'^', views.index, name='home'),
]

if settings.DEBUG:
    

    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
admin.site.site_header = "IIITDMJ Alumni Association"
admin.site.site_title = "Alumni Association"
admin.site.index_title = "Alumni Association Admin"
