"""
https://www.codingforentrepreneurs.com/blog/custom-analytics-with-django/#watch

"""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .utils import get_client_ip
from .signals import object_viewed_signal

from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from users.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist

User = settings.AUTH_USER_MODEL


class ObjectViewed(models.Model):
    """
    track hte user movements
    """
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_obj = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s viewed on %s" % (self.content_obj, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    # print(sender)
    # print(instance)
    # print(request)
    # print(request.user)

    c_type = ContentType.objects.get_for_model(sender)
    object_viewed_obj = ObjectViewed.objects.create(
        user=request.user,
        ip_address=get_client_ip(request),
        object_id=instance.id,
        content_type=c_type
    )


object_viewed_signal.connect(object_viewed_receiver)


class UsersSessions(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"session for {self.user}"

    def end_session(self):
        session_key = self.session_key
        session = Session.objects.filter(pk=session_key)

        try:
            if session.filter():
                session.first().delete()
            self.active = False
            self.save()

        except ObjectDoesNotExist:
            pass

        return self.active


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    session_key = request.session.session_key
    ip_address = get_client_ip(request)
    user = instance

    UsersSessions.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )


user_logged_in.connect(user_logged_in_receiver)


# make sure that user have only one at the time session active
def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UsersSessions.objects.filter(user=instance.user, active=True).exclude(pk=instance.pk)

        for q in qs:
            q.end_session()
            q.save()


post_save.connect(post_save_session_receiver, sender=UsersSessions)
