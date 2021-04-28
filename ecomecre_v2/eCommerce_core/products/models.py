from django.db import models
from PIL import Image
import os
from django.utils import timezone
from django.urls import reverse
import uuid
from django.db.models import Q
from django.conf import settings

User = settings.AUTH_USER_MODEL


def customer_image_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('upload/products_img/', filename)


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):

    def get_by_id(self, pk):
        qs = self.get_queryset().filter(pk=pk)
        if qs.count() == 1:
            return qs.first()
        return None

    @property
    def featured(self):
        return self.get_queryset().filter(featured=True)

    def get_queryset(self):
        # enable costume query set
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        # redefine all()
        return self.get_queryset().active()

    def search(self, query, featured=None):
        lookup = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query) |
                Q(tags__title__icontains=query)

        )

        if query:
            if featured:
                # featured as property
                return Product.objects.featured.active().filter(lookup).distinct()
            # active as top level class (same job line)
            return Product.objects.filter(lookup).active().distinct()

        if featured:
            return Product.objects.featured.active().all()
        return Product.objects.all()


class Product(models.Model):
    objects = ProductManager()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product", default=User)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)  # 12345.12
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg',
                              upload_to=customer_image_file_path)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

    def __str__(self):
        return f"( pk:{self.pk} product :: {self.title}) "

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-timestamp", "price", ]

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)
            output_size = (300, 300)

            if img.height > 300 or img.width > 300:
                img.thumbnail(output_size)
                img.save(self.image.path)
        except IOError:
            print(f'where is the file for img working ?')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        ordering = ["-timestamp", ]

    def __str__(self) -> str:
        return "comment for -> " + str(self.product.title)

# todo like
