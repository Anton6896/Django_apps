from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)  # stripe cents

    def __str__(self):
        return str(self.name)

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
