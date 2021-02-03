from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import os
import uuid


def customer_image_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('upload/customer/', filename)


class CustomUser(AbstractUser):

    class Meta:
        db_table = 'CustomUser'
        verbose_name = 'custom_user'
        verbose_name_plural = 'custom_users'

    # my additional fields in here
    image = models.ImageField(default='default.jpg',
                              upload_to=customer_image_file_path)
    building_community_name = models.CharField(
        max_length=200, default='no_name_')
    full_address = models.CharField(max_length=255, default='no_address_')
    is_voted = models.BooleanField(default=False)
    apartment = models.IntegerField(default=0)

    ROLE_CHOICES = (
        ('tenant', 'tenant'),
        ('committee', 'committee'),
    )

    role = models.CharField(
        choices=ROLE_CHOICES, blank=True, null=True, max_length=20)

    def __str__(self):
        return "[ " + self.username + " from building : " + self.building_community_name + " ]"

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)
            output_size = (300, 300)

            if img.height > 300 or img.width > 300:
                img.thumbnail(output_size)
                img.save(self.image.path)
        except IOError:
            print(f'where is the file for img working ?')

    def is_tenant(self):
        return self.role == 'tenant'
