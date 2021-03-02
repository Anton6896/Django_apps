from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.dispatch import Signal


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # create db instance 
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # save db instance 
    instance.profile.save()


"""
track user session in analytics app 
send signal of user sessions users.view -> login view
"""
user_logged_in = Signal(providing_args=['instance', 'request'])
