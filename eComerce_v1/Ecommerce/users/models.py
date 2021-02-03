from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    # extend user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # todo add picture etc

    def __str__(self) -> str: return f'{self.user.username} profile.'
