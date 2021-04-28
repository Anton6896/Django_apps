from django.utils import timezone
from django.db import models
from products.models import Product


class Tag(models.Model):
    title = models.CharField(max_length=120)
    timestamp = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    product = models.ManyToManyField(Product, blank=True, related_name="tags")

    def get_amount(self):
        return self.product.count()

    def __str__(self):
        return f"Tag :: {self.title} [{self.get_amount()}]"
