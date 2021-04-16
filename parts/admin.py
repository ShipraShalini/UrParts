from django.contrib import admin

from parts.models import Part


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("manufacturer", "category", "model", "part", "part_category")
    search_fields = ("manufacturer", "category", "model", "part", "part_category")
    list_filter = ("manufacturer", "category", "model")
    readonly_fields = ("uuid", "created_at")
