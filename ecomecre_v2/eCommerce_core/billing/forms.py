from django import forms
from .models import BillingAddress


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ('address_1_b',
                  'address_2_b',
                  'city_b',
                  'country_b',
                  'postcode_b',
                  )
