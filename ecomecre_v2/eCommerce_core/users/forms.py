from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


class RegisterForm(forms.Form):

    username = forms.CharField(
        label='Username',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "username",
                "class": "form-control",
                "placeholder": "username",
                "aria-label": "First name",
            }
        ))

    email = forms.EmailField(
        label='Username',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "placeholder": "email",
                "aria-label": "Last name",
            }
        ))

    password = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "id": "formGroupExampleInput",
                "placeholder": "password",
            }
        ))

    password2 = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "id": "formGroupExampleInput2",
                "placeholder": "confirm password",
            }
        ))

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password != password2:
            print("=======================================")
            raise forms.ValidationError("password noy match !")
        return data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_model = get_user_model()

        try:
            user_model.objects.get(username__iexact=username)
        except user_model.DoesNotExist:
            return username

        raise forms.ValidationError(("This username has already existed."))


class LogInForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "username",
                "class": "form-control",
                "id": "floatingInput",
                "placeholder": "Username",
                "name": 'username',
            }
        ))

    password = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "name": 'password',
                "type": "password",
                "class": "form-control",
                "id": "floatingPassword",
                "placeholder": "Password",
            }
        ))


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'address_1',
            'city',
            'country',
            'postalcode',
            'billing_is_shipping',
        )
