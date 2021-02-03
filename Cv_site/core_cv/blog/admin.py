from django.contrib import admin
from . import models


class BlogModelAdmin(admin.ModelAdmin):
    list_display = ['pk', "title", "created_at"]
    list_display_links = ['pk', "title"]


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['pk', "created_at", "author"]
    list_display_links = ['pk', ]


admin.site.register(models.Blog, BlogModelAdmin)
admin.site.register(models.BlogComment, CommentModelAdmin)
