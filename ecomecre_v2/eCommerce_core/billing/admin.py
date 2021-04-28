from django.contrib import admin
from .models import BillingProfile, BillingAddress

admin.site.register(BillingProfile)
admin.site.register(BillingAddress)
