from django.contrib import admin
from . import models


def make_refound_accepted(modeladmin, request, queryset):
    queryset.update(refound_granted=True)


make_refound_accepted.short_description = 'Update: refound granted'


class OrderAdmin(admin.ModelAdmin):
    # admin panel customization for treking the order status
    tot_price = models.Order.get_total

    actions = [make_refound_accepted]

    list_display = [
        'user',
        'ordered',
        tot_price,
        'being_delivered',
        'received',
        'refound_requested',
        'refound_granted',
        'billing_address',
        'shipping_address',
        'payment',
        'coupon',
    ]

    list_display_links = [
        'user',
        'billing_address',
        'shipping_address',
        'payment',
        'coupon',

    ]

    list_filter = [
        'ordered',
        'being_delivered',
        'received',
        'refound_requested',
        'refound_granted',

    ]

    search_fields = [
        'user__username',
        'ref_code',
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default',

    ]
    list_filter = [
        'default',
        'address_type',
        'country',
    ]
    search_fields = [
        'user__username',
        'street_address',
        'apartment_address',
        'zip',

    ]


admin.site.register(models.Item)
admin.site.register(models.Coupon)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem)
admin.site.register(models.Payment)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Refound)
