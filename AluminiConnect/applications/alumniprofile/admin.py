from django.contrib import admin
from .models import Profile, Constants, Batch

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'sex', 'roll_no', 'batch', 'programme', 'branch')
    ordering = [('roll_no'),]

class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch',)
    ordering = [('batch'),]

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Batch, BatchAdmin)
