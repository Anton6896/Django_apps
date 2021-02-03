from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import CustomUser


class SighUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')


# class UserRegisterForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserRegisterForm, self).__init__(*args, **kwargs)
#         self.fields['password1'].widget.attrs["placeholder"] = "Enter Password"
#         self.fields['username'].widget.attrs["placeholder"] = "UserName"

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2']

#     email = forms.EmailField(
#         widget=forms.EmailInput(
#             attrs={
#                 "name": "email",
#                 "id": "email",
#                 "placeholder": "Your Email *"
#             }
#         )
#     )
