from .models import Mesage
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Mesage)
def update_tag_field(sender, instance: Mesage, created, **kwargs):
    if created:
        if instance.tag == 'message':
            instance.status = 'done'
            instance.save()
