from django.contrib import admin
from core.models import *

# Register your models here.

class ShowAdmin(admin.ModelAdmin):
    list_display = (
                    'name',
                    'quiz_time'
                    )
admin.site.register(Show, ShowAdmin)

admin.site.site_header = 'Quiz Admin Panel '
