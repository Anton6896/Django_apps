from django.contrib import admin
from tags.models import Tag


class CostumeTag(admin.ModelAdmin):
    list_display = ("__str__", 'active')
    list_display_links = ("__str__", 'active')


admin.site.register(Tag, CostumeTag)
