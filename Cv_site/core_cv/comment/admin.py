from django.contrib import admin
from .models import Comment


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'content_object', 'timestamp', 'parent']
    list_display_links = ['pk', 'content_object']
    list_filter = ["timestamp"]


admin.site.register(Comment, CommentModelAdmin)
