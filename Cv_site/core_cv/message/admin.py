from django.contrib import admin
from .models import Mesage


class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['pk', "title", 'tag', "timestamp", 'status']
    list_display_links = ["timestamp", 'tag', ]
    list_filter = ["timestamp", 'is_read' ]
    search_fields = ["title", "content", ]
    list_editable = ["title"]

    class Meta:
        model = Mesage


admin.site.register(Mesage, MessageModelAdmin)

