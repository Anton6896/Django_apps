from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # signal activation 
    def ready(self):
        import users.signals
