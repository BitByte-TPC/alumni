from django.contrib import admin
from .models import Event, Attendees


class EventAdmin(admin.ModelAdmin):
    list_display = ('title_stripped', 'start_date', 'end_date', 'location', 'is_completed')
    ordering = [('start_date'), ]


class AttendeesAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'event_id')


admin.site.register(Event, EventAdmin)
admin.site.register(Attendees, AttendeesAdmin)
