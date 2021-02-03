from django import forms
from django.contrib import messages
from django.forms import widgets
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_OPTIONS = (
    ('debit', 'Debit'),
    ('paypal', 'Paypal')
)


class CheckoutForm(forms.Form):
    # adjust form for the checkout.html
    street_address = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={
            'placeholder': '1234 Main St',
            'class': 'form-control'
        })
    )
    apartment_address = forms.CharField(
        max_length=200, required=False, widget=forms.TextInput(
            attrs={
                'placeholder': 'Apartment or suite',
                'class': 'form-control'
            }
        )
    )
    country = CountryField(blank_label='(select country)').formfield(
        # have an special widget place ( CountrySelectWidget )
        widget=CountrySelectWidget(
            attrs={
                'class': 'custom-select d-block w-100',
                'id': 'country',
            }
        )
    )

    zip = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'placeholder': 'zip',
            'class': 'form-control',
            'type': 'text',
            'id': 'zip'
        }
    ))
    same_shipping_address = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'custom-control-input',
                'id': 'same-address',
                'type': 'checkbox'
            }
        ), required=False
    )
    save_info = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                # connection to html file
                'class': 'custom-control-input',
                'id': 'save-info',
                'type': 'checkbox'
            }
        ), required=False
    )
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT_OPTIONS)


class CouponForm(forms.Form):
    code = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Promo code',
                'type': 'text',
                'aria-label': 'Recipient\'s username',
                'aria-describedby': 'basic-addon2'
            }
        )
    )


class RefoundForm(forms.Form):
    ref_code = forms.CharField(max_length=20)
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "cols": 10}))
    email = forms.EmailField()



