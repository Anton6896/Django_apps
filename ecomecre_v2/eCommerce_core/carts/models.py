from decimal import Decimal
from django.db import models
from products.models import Product
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed
from django.urls import reverse


class CartManager(models.Manager):

    def create_cart(self, user):
        if user and user.is_authenticated:
            return self.model.objects.create(user=user)
        return self.model.objects.create(user=None)

    def get_cart(self, request):
        """
        if user already have an cart then return his cart
        else new cart to user

        if user in incognito add staff to cart and his cart was empty then return new card
        else (todo add to old cart, make transfer of new products to old card )
        return users old card without new products !
        """
        cart_pk = request.session.get("cart_pk", None)

        if request.user.is_authenticated:
            # check if user already have cart
            qs = Cart.objects.filter(user=request.user)
            if qs:
                cart = qs.first()
                if cart.get_amount() == 0:
                    pass
                else:
                    return cart

        if cart_pk:
            # get cart to user if he created one
            cart_obj = Cart.objects.get(pk=cart_pk)

            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()

        else:
            # cart creation
            print("create new cart_pk")
            cart_obj = Cart.objects.create_cart(request.user)
            request.session['cart_pk'] = cart_obj.pk

        return cart_obj


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='cart', null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='cart', blank=True)
    total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)  # on create
    updated = models.DateTimeField(auto_now=True)  # on edit
    objects = CartManager()
    tax = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)

    def get_amount(self):
        return self.products.count()

    def get_total_tax_price(self):
        return self.total + self.tax

    def __str__(self):
        return f"[ cart : {self.pk} , tot_price : {self.total} , prod_count > {self.get_amount()} ]"

    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)
        pass

    def get_absolute_url(self):
        # back end will find an right card for user -> def get_cart(self, request):
        return reverse("cart:cart_home")


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    # count total sum (money) of all products in cart
    # https://docs.djangoproject.com/en/3.1/ref/signals/#m2m-changed
    if action == "post_remove" or action == "post_add" or action == "post_clear":
        # after change check the sum of all products
        products = instance.products.all()
        tot = 0
        for p in products:
            tot += p.price
        instance.total = tot
        instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_tax_receiver(sender: Cart, instance: Cart, *args, **kwargs):
    # get amount of tax for all products in cart
    if instance.total > 0:
        instance.tax = (instance.total * Decimal(0.15)) + instance.total

    else:
        instance.tax = 0


pre_save.connect(pre_save_tax_receiver, sender=Cart)
