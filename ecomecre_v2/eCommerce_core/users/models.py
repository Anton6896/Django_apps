# costume profile for ech user that was created
from django.db import models
from PIL import Image
import os
from uuid import uuid4
from django.core.validators import MinValueValidator

from django.conf import settings
User = settings.AUTH_USER_MODEL

"""
https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model
"""


def customer_image_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.{ext}'

    return os.path.join('upload/customer_pic/', filename)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpg',
                              upload_to=customer_image_file_path)

    # this address fields is for shipment location of user
    # can call this address as -> ShippingAddress
    address_1 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    postalcode = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)])
    billing_is_shipping = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)
            output_size = (300, 300)

            if img.height > 300 or img.width > 300:
                img.thumbnail(output_size)
                img.save(self.image.path)
        except IOError:
            print(f'where is the file for img working ?')

    def __str__(self):
        return f"profile of {self.user.username}"
