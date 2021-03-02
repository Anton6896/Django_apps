from django.contrib import admin
from .models import ObjectViewed, UsersSessions


class SessionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "timestamp", "active")
    list_display_links = ("__str__",)


admin.site.register(ObjectViewed)
admin.site.register(UsersSessions, SessionAdmin)
