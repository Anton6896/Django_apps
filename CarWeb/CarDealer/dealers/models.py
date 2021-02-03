from django.db import models


class Dealer(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    email = models.EmailField(max_length=150)

    def __str__(self):
        return f'{self.name} dealer'
