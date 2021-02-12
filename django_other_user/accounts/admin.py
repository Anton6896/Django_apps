from django.contrib import admin
from .forms import UserAdminChangeForm, UserAdminCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


# critical to use BaseUserAdmin as class to derive from !!
class CustomUserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('__str__', 'staff', 'active', 'admin')
    list_filter = ('staff', 'active', 'admin')

    readonly_fields = ('timestamp',)
    fieldsets = (
        ('main', {'fields': ('email', 'password', 'username', 'full_name', 'timestamp',)}),
        ('Permissions', {'fields': ('staff', 'active', 'admin')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1',)}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
