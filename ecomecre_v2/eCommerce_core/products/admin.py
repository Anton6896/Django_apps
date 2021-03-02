from django.contrib import admin
from .models import Product, Comment


class CustumeProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "featured", "active",)
    list_display_links = ("title",)
    search_fields = ("title", "price", "id", "featured", "active",)
    list_editable = ("price", "featured", "active",)


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "product", "timestamp", "user"]
    list_display_links = ["pk", "product", ]


admin.site.register(Product, CustumeProductAdmin)
admin.site.register(Comment, CommentModelAdmin)
