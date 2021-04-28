from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class BillingProfile(models.Model):
    # related_query_name -> User.objects.filter(billing_profile=user.instance) to get BillingProfile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True,
                                blank=True, on_delete=models.CASCADE,
                                unique=True, related_query_name='billing_profile')
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    # stripe is costumer_id
    costumer_id = models.CharField(max_length=200, null=True, blank=True)

    """
    i will put the shipping address in users app (Profile)
    and billing address will be here in BillingProfile
    """

    def __str__(self):
        return f"pk:{self.pk} :: Billing profile - {str(self.email)}"


# create an BillingProfile at user creation
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        costumer = stripe.Customer.create(
            email=instance.email,
            description=f"eCom costumer for testing only ! : ({str(instance)}) "
        )  # stripe costumer

        BillingProfile.objects.get_or_create(
            user=instance,
            email=instance.email,
            costumer_id=costumer.id
        )


post_save.connect(user_created_receiver, sender=settings.AUTH_USER_MODEL)


class BillingAddress(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,
                                        on_delete=models.CASCADE,
                                        related_name='billing_profile')
    address_1_b = models.CharField(max_length=250, null=True, blank=True)
    address_2_b = models.CharField(max_length=250, null=True, blank=True)
    city_b = models.CharField(max_length=50, null=True, blank=True)
    country_b = models.CharField(max_length=50, null=True, blank=True)
    postcode_b = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

    def __str__(self) -> str:
        return f"billing address of {self.billing_profile.user.username}"
