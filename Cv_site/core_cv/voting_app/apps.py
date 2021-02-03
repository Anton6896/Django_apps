from django.apps import AppConfig


class VotingAppConfig(AppConfig):
    name = 'voting_app'

    def ready(self):
        import voting_app.signals


