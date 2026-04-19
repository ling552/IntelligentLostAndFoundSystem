from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "title", "category", "location", "time", "status", "user", "created_at")
    list_filter = ("type", "category", "status")
    search_fields = ("title", "description", "location", "contact", "user__username")
    ordering = ("-created_at",)
