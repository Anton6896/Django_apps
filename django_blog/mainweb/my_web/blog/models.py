from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# don't forger to register the model 
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # delete the post if has no user to belonged to
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # where to redirect after the post was created 
    def get_absolute_url(self):
        return reverse('blog-post-detail', kwargs={'pk':self.pk})