from django.contrib import admin
from .models import Visitor, VisitorImage


class VisitorImageInline(admin.TabularInline):
    model = VisitorImage
    extra = 1


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("name", "resident", "home_number", "license_plate", "status", "created_by", "created_at")
    list_filter = ("status", "resident", "created_at")
    search_fields = ("name", "license_plate", "resident__username", "resident__name", "home_number")
    inlines = [VisitorImageInline]