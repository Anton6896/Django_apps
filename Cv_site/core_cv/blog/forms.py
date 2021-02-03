from django import forms
from django.forms.widgets import Textarea
from . import models


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "col-sm-12",
            'placeholder': "Your Comment",
        }
    ))
