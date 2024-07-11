from django.contrib import admin
from .models import Blog


from applications.blog.models import Blog, Campaign, Replies

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'blog_id', 'title', 'author', 'date_added', 'updated_at', 'blog_type', 'campaign_id',
    )
    ordering = [('-date_added'), ]
    search_fields = ['blog_id', 'title', 'author', 'blog_type', 'campaign_id']
    
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        'campaign_id', 'name', 'date_started', 'date_ended',
    )
    ordering = [('-date_started'), ]
    search_fields = ['campaign_id', 'name',]

class RepliesAdmin(admin.ModelAdmin):
    list_display = (
        'reply_id', 'blog_id', 'sender', 'receiver', 'time_stamp',
    )
    ordering = [('-time_stamp')]
    search_fields = ['sender', 'blog_id']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Replies, RepliesAdmin)
