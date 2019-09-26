from django.contrib import admin
from session.models import SessionModel, LastDataModel


admin.site.register(LastDataModel)


class SessionAdmin(admin.ModelAdmin):
    list_display = ('is_booked','salon','is_ready', 'day', 'time','price',)
    list_filter = ('is_booked','salon','is_ready', 'day', 'time','price',)   
    search_fields = ('is_booked','salon','is_ready', 'day', 'time','price',)


admin.site.register(SessionModel,SessionAdmin)
