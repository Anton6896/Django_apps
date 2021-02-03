from django.apps import AppConfig
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from .models import CustomUser as User
        from . signals import add_to_group
        post_save.connect(add_to_group, sender=User)
