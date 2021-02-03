from django.db import models
from django.utils import timezone
from accounts.models import CustomUser as User
from django.urls import reverse


class Voting(models.Model):
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    counter_positive = models.IntegerField(default=0)
    counter_negative = models.IntegerField(default=0)
    counter_neutral = models.IntegerField(default=0)

    def __str__(self):
        return self.short_description + " , date created : " + str(self.date_posted)

    def get_absolute_url(self):
        return reverse('voting', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "voting"
        db_table = 'voting'
        verbose_name_plural = "voting_s"


class VotingChoices(models.Model):
    class Meta:
        verbose_name = "voting_choice"
        db_table = 'voting_choice'
        verbose_name_plural = 'voting_choices'

    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='voting_class')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote_user')

    VOTING_CHOICES = (
        ('yes', 'yes'),
        ('no', 'no'),
        ('pass', 'pass')
    )
    voting_choice = models.CharField(
        choices=VOTING_CHOICES, blank=True, null=True, max_length=6, default='pass')

    def __str__(self):
        return "pk: " + str(self.pk) + " -> " + self.voting.short_description + ".. user: " + self.user.username

    def save(self, *args, **kwargs):
        super(VotingChoices, self).save(*args, **kwargs)

        v: Voting = Voting.objects.filter(pk=self.voting.pk).first()

        if self.voting_choice == 'yes':
            v.counter_positive += 1
            v.save()
        elif self.voting_choice == 'no':
            v.counter_negative += 1
            v.save()
        else:
            v.counter_neutral += 1
            v.save()
