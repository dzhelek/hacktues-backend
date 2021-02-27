from django.contrib import admin

from . import models

@admin.register(models.Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = 'id', 'full_name', 'email', 'phone', 'elsys', 'tshirt_size'
    list_filter = 'tshirt_size', 'elsys'
    readonly_fields = 'id',
    filter_horizontal = 'technologies',
