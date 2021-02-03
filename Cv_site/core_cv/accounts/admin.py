from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import SighUpForm


class CustomUserAdmin(UserAdmin):
    add_form = SighUpForm
    model = CustomUser
    list_display = ['pk', 'email', 'username', 'role']
    list_filter = ('role',)
    list_display_links = ['pk','email', 'username', ]

    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            # group heading of your choice; set to None for a blank space instead of a header
            'Custom Field Heading',
            {
                'fields': (
                    'role',
                    'image',
                    'building_community_name',
                    'full_address',
                    'is_voted',
                    'apartment',
                ),
            },
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
