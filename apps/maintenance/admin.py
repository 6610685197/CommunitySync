from django.contrib import admin
from .models import MaintenanceRequest

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "resident", "title", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "resident__username", "resident__name")