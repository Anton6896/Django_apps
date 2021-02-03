from .models import Voting, VotingChoices
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Voting)
def create_vote(sender, instance, created, **kwargs):
    if created:
        # create db instance
        v = VotingChoices.objects.create(
            voting=instance, user=instance.user, voting_choice='pass')
        v.save()
