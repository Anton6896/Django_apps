from django.db import models
from accounts.models import CustomUser
from PIL import Image
from django.utils import timezone
import markdown
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType


# todo create the schedule task that check if Message (issue tag)
#  is created more than one week -> send message to user (admin)
#  >>> after research the task can be implemented with Django+Celery
# https://medium.com/@kevin.michael.horan/scheduling-tasks-in-django-with-the-advanced-python-scheduler-663f17e868e6#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjZhZGMxMDFjYzc0OThjMDljMDEwZGMzZDUxNzZmYTk3Yzk2MjdlY2IiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2MDg4OTMzODksImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExMTA5ODc2NDY0MzM0MjcwMzQzMSIsImVtYWlsIjoiYW50b242ODk2QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhenAiOiIyMTYyOTYwMzU4MzQtazFrNnFlMDYwczJ0cDJhMmphbTRsamRjbXMwMHN0dGcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJuYW1lIjoiQW50b24gUiIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS0vQU9oMTRHZ0txaG9ZOFZVVWdKTzJtSWV5UWFvMkx0UWlSc3NzU1h3OTZxRHFzc2c9czk2LWMiLCJnaXZlbl9uYW1lIjoiQW50b24iLCJmYW1pbHlfbmFtZSI6IlIiLCJpYXQiOjE2MDg4OTM2ODksImV4cCI6MTYwODg5NzI4OSwianRpIjoiZTAzYjlkMjRlOTc4NWYxMTgwMDFlNmYxYWRhZjVkNjc2ODdjMjYzYyJ9.UE-jMYuwkDViyJlXXb79ZHusV54P9J5TKI8Fv4fCZkrleDg5vNMU6KaBW47tVgbx5LDSEefZQzGKvZzRrMqF1uq8vi3h4v0_1dwqjpneEX24zH_ieBLWhGditbwpuurgtoEwSqPZnu5NFlqdF5rJFHotTykh6I-gX4-n4v_Grf_MoqYqxAafWutyWib0A5KNz_nVr8tUGRbAcrN6-u2mnhPcRuR2r5IiPTNL90hipUFueBtz7Our4IewvrqnEiQUg6ANowPIvLLnCuQ7SjadTO98wwiBYgb_H_SgESaSTYxsN80RBKb38wVuKdXBQ9kXnvVEaVeYXR1ub6hthiO4-g


def customer_image_file_path(instance, filename):
    import os
    import uuid
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('upload/message_pic/', filename)


class MessageManager(models.Manager):
    """
    is an manager :
    Message.objects.all()
    Message.objects.crete(author=user, title=title etc...)
    etc...

    """

    # override the all method (shew only un read messages)
    # def all(self, *args, **kwargs):
    #     return super(MessageManager, self).filter(is_read=False)
    pass


class Mesage(models.Model):
    objects = MessageManager()  # activate manager
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # slug -> for link instead of pk (still dont know if i want to use it) ?
    # slug = models.SlugField(unique=True)
    image = models.ImageField(default='default.jpg',
                              upload_to=customer_image_file_path)
    created_at = models.DateTimeField(default=timezone.now)
    # update update time for message
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    content = models.TextField()
    priority = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)

    STATUS_CHOICES = (
        ('done', 'done'),
        ('working_on', 'working_on'),
        ('on_hold', 'on_hold'),
    )
    TAG_CHOICES = (
        ('message', 'message'),
        ('issue', 'issue'),
    )
    tag = models.CharField(choices=TAG_CHOICES,
                           max_length=15, default='message')
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=15, default='working_on')

    def save(self, *args, **kwargs):
        super(Mesage, self).save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)
            output_size = (300, 300)

            if img.height > 300 or img.width > 300:
                img.thumbnail(output_size)
                img.save(self.image.path)
        except IOError:
            print(f'where is the file for img working ?')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("message:detail", kwargs={"pk": self.pk})

    def is_pass_week(self):
        # this is util function for requirement to
        # send notification if pass a week in issue message
        return timezone.now() == self.created_at + timezone.timedelta(days=7)

    def is_issue(self):
        return self.tag == 'issue'

    def get_markdown(self):
        md = markdown.Markdown()
        return md.convert(self.content)

    def __str__(self):
        if self.is_issue():
            return f'issue: {self.pk}, title: {self.title}, \tby: {self.author.username}'
        else:
            return f'message: {self.pk}, title: {self.title}, \tby: {self.author.username}'

    @property
    def comments(self):
        # now message.comments  -> all comments for this message as queryset
        return Comment.objects.filter_by_instance(self)

    @property
    def get_content_type(self):
        """
           instance = get_object_ot_404(Message)
           {
               "content_type":instance.get_content_type,
               etc ...
           }
           """
        return ContentType.objects.get_for_model(self.__class__)

    class Meta:
        ordering = ["-timestamp", "-created_at"]
        db_table = 'messages'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
