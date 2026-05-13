from django.contrib import admin
from .models import GemListing


@admin.register(GemListing)
class GemListingAdmin(admin.ModelAdmin):
    list_display = (
        "gem_id",
        "name",
        "variety",         # Added
        "color",           # Added
        "carat",
        "price",
        "owner_id",
        "location",
        "status",
        "created_at",
        "certificate_url"  # Added
    )
    
    search_fields = ("name", "owner_id", "location", "status", "variety", "color")
    list_filter = ("status", "variety", "color", "created_at", "location")
    ordering = ("-created_at",)
    readonly_fields = ("gem_id", "created_at")