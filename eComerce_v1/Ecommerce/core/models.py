from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.core.files.storage import FileSystemStorage
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fs = FileSystemStorage(
    location=(os.path.join(BASE_DIR, 'media/profile_pics/')))


# Core models

CATEGORY_CHOICES = (
    # first to db second to html
    ('shirt', 'Shirt'),
    ('sport_wear', 'Sport wear'),
    ('outwear', 'Outwear'),
)

LABEL_CHOICES = (
    # first to db second to html
    ('primary', 'primary'),
    ('secondary', 'secondary'),
    ('danger', 'danger'),
    ('no_label', 'no_label')
)

ADDRESS_CHOICES = (
    ('billing', 'billing'),
    ('shipping', 'shipping')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=50, default='undefined_thing')
    labels = models.CharField(choices=LABEL_CHOICES,
                              max_length=50, default='no_label')
    description = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # can add the time addad to the web for the ordering ! optional

    def __str__(self) -> str: return self.title

    def get_absolute_url(self):
        return reverse('core:product', kwargs={'pk': self.pk})

    def get_add_to_card_url(self):
        return reverse('core:add_to_card', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    # connector between the order and the item
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str: return f'{self.item.title} has {self.quantity}'

    def total_price(self) -> float:
        if self.item.discount_price:
            return self.quantity * self.item.discount_price
        else:
            return self.quantity * self.item.price


class Order(models.Model):
    # order holds the order items as many to many
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    # connect order to billing and payment
    billing_address = models.ForeignKey(
        'Address',
        related_name='billing_address',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    shipping_address = models.ForeignKey(
        'Address',
        related_name='shipping_address',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True
    )
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True
    )

    '''
    order life cycle 
    (how do i like to track the package life ? )

    1. add item to card 
    2. add billing address 
    ( fail checkout ?)
    3. payment 
    (preprocessing , processing etc of package it self )
    4. being delivered 
    5. received 
    6. refunds 
    '''
    ref_code = models.CharField(max_length=20, default=000)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refound_requested = models.BooleanField(default=False)
    refound_granted = models.BooleanField(default=False)

    def __str__(self) -> str: return f'{self.user.username} order'

    def get_absolute_url(self):
        return reverse('core:order_summary', kwargs={'pk': self.pk})

    def get_total(self) -> float:
        total = 0
        for order_item in self.item.all():
            total += order_item.total_price()

        # get discount for the coupon
        if self.coupon:
            total = total - ((total / 100) * self.coupon.percentage)
            # can add the coupon validation procedure here

        return total


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    zip = models.IntegerField(default=000000)
    address_type = models.CharField(max_length=20, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Addresses'


    def __str__(self) -> str: return f'address: {self.street_address}'


class Payment(models.Model):
    # save payment transactions
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str: return f'{self.user.username} payment . '


class Coupon(models.Model):
    # discount codes
    code = models.CharField(max_length=15)
    active = models.BooleanField(default=True)
    percentage = models.IntegerField(default=1)

    def __str__(self) -> str: return self.code


class Refound(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    mail = models.EmailField(null=True)

    def __str__(
        self) -> str: return f'refound order ref code : {self.order.ref_code}'
