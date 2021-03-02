from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from .utils import Mailchimp

User = settings.AUTH_USER_MODEL


class MarketingPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='marketing')
    subscribed = models.BooleanField(default=True)
    subscription_test = models.BooleanField(default=True)
    mailchimp_message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


def market_pref_create_receiver(sender, instance: MarketingPreference, created, *args, **kwargs):
    """
    add user to mailchimp subscription
    """
    if created:
        status_code, res = Mailchimp().add_email(instance.user.email)
        print(f'chimp status code {status_code}, data::\n{res}')


post_save.connect(market_pref_create_receiver, sender=MarketingPreference)


def market_pref_receiver(sender, instance: User, created, *args, **kwargs):
    if created:
        MarketingPreference.objects.get_or_create(user=instance)


post_save.connect(market_pref_receiver, sender=User)


def market_pref_update_receiver(sender, instance: MarketingPreference, *args, **kwargs):
    """
    any change on subscription will effect the mailchimp subscription
    subscription test is local test value - subscribed represent foreign value from mailchimp
    """
    if instance.subscribed != instance.subscription_test:
        if instance.subscribed:
            status_code, res = Mailchimp().subscribe(instance.user.email)
        else:
            status_code, res = Mailchimp().unsubscribe(instance.user.email)

        if res['status'] == 'subscribed':
            instance.subscribed = True
            instance.subscription_test = True
            instance.mailchimp_message = res
        else:
            instance.subscribed = False
            instance.subscription_test = False
            instance.mailchimp_message = res


pre_save.connect(market_pref_update_receiver, sender=MarketingPreference)
