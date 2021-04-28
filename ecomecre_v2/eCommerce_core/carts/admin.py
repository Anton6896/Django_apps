from django.contrib import admin
from .models import Cart


class CostumeCart(admin.ModelAdmin):
    list_display = ("__str__", "timestamp", "updated")
    list_display_links = ("__str__",)
    search_fields = ("total", "pk", "user__username", "timestamp", "products__title")


admin.site.register(Cart, CostumeCart)
