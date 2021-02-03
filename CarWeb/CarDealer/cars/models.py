from django.db import models
import datetime
from dealers.models import Dealer
from django.urls import reverse


all_years = [
    (r, r) for r in range(2000, datetime.date.today().year+2)
]
default_year = datetime.datetime.now().year
car_gear = [
    ('manual', 'manual'),
    ('automatic', 'automatic')
]
car_category = [
    ('used', 'used'),
    ('new', 'new')
]


class Car(models.Model):
    '''
    for this tutorial i will use the miles as equation point for the 
    index page at lowest miles at the car , actually is better to do that with date field 
    '''
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=32, choices=car_category)
    image1 = models.ImageField(upload_to='images')
    image2 = models.ImageField(upload_to='images', blank=True)
    image3 = models.ImageField(upload_to='images', blank=True)
    miles = models.IntegerField(blank=False, null=False, default=0)
    transmission = models.CharField(
        max_length=32, choices=car_gear)
    year = models.IntegerField(
        choices=all_years, default=default_year
    )
    power = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(
        blank=True, max_digits=5, decimal_places=2, null=True)
    description = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'car: {self.brand} is {self.category}'

    def get_absolute_url(self):
        return reverse('car_detail', kwargs={
            'pk':self.pk
        })
