from django.contrib import admin
from .models import MarketingPreference


class MarketAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated', 'mailchimp_message', ]
    list_display = ['__str__', 'subscribed', 'updated']

    class Meta:
        model = MarketingPreference
        fields = [
            'user',
            'subscribed',
            'subscription_test',
            'mailchimp_message',
            'timestamp',
            'updated',
        ]


admin.site.register(MarketingPreference, MarketAdmin)
