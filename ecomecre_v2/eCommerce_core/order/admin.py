from django.contrib import admin

from .models import Order


class CostumeOrder(admin.ModelAdmin):
    list_display = ("pk", "order_id", "cart", "total", "status", "active", "timestamp")
    list_display_links = ("pk", "order_id", "cart",)
    search_fields = ("pk", "order_id", "cart", "status", "active",)
    list_editable = ("active", "status",)
    list_filter = ("status", "active",)


admin.site.register(Order, CostumeOrder)
