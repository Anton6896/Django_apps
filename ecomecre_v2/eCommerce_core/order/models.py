from django.db import models
from carts.models import Cart
from django.db.models.signals import pre_save, post_save
from eCommerce_core.utils import unique_order_id_generator
from billing.models import BillingProfile
from users.models import Profile as ShippingAddress
from billing.models import BillingAddress

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    """
    order creation : on button checkout will be created unique order  
    after check out process set active=False and store order for history 

    ***
        this is bad approch fo me ! i didnt see any items in order ,
        but for this practice lessons only , ( good , is to store :
        cart (as unique to all users )
        order 
        order_item (have amount)
        checkout_form (billing etc)
    ***
    """
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=20, default='created', choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    # shipping_total -> must be rearrange for all user -> check_shipping_price()
    # depend on shipping place for now is static (6.00 $)
    shipping_total = models.DecimalField(
        default=6.00, max_digits=50, decimal_places=2)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # update on creation
    updated = models.DateTimeField(auto_now=True)  # update on modification

    # billing profile and additional addresses
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.SET_NULL,
                                        null=True, related_name='billing')
    shipping_address = models.ForeignKey(ShippingAddress, null=True, blank=True, on_delete=models.SET_NULL)
    billing_address = models.ForeignKey(BillingAddress, null=True, blank=True, on_delete=models.SET_NULL)

    # =================

    def __str__(self):
        return f"[order: {self.order_id}] "

    def update_total(self):
        self.total = self.cart.tax
        self.save()
        return self.total


def pre_save_order_id_receiver(sender: Order, instance: Order, *args, **kwargs):
    """
    on order create : get unique order_id , get total sum + tax from the card 
    """
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

        # if user have any other orders beside this one set active=False
        qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
        if qs.exists():
            qs.update(active=False)


pre_save.connect(pre_save_order_id_receiver, sender=Order)


def pre_save_order_total(sender: Order, instance: Order, *args, **kwargs):
    cart_obj = instance.cart
    if cart_obj:
        instance.total = cart_obj.tax


pre_save.connect(pre_save_order_total, sender=Order)


# after save() in cart table , update the Order.total value
def post_save_order_total_update(sender, instance: Cart, created, *args, **kwargs):
    if not created:
        qs = Order.objects.filter(cart__pk=instance.pk)
        if qs:
            order = qs.first()
            order.update_total()


post_save.connect(post_save_order_total_update, sender=Cart)
