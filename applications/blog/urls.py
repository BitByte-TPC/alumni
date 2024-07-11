from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [

    path('', views.index, name='index'),
    path('<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('newBlog/', views.blog_create, name='blog_create'),
    path('<int:blog_id>/edit/', views.blog_update, name='blog_update'),
    path('<int:blog_id>/delete/', views.blog_delete, name='blog_delete'),
    path('<int:reply_id>/deleteReply/', views.reply_delete, name='reply_delete'),
    
    path('newCampaign/', views.campaign_create, name='campaign_create'),
    path('<int:campaign_id>/deleteCampaign/', views.campaign_delete, name='campaign_delete'),
    path('<int:campaign_id>/updateCampaign/', views.campaign_update, name='campaign_update'),
    path('<int:campaign_id>/Campaign/', views.campaign_detail, name='campaign_detail'),
]