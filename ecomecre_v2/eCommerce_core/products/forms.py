from django import forms
from .models import Comment


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "form-control",
            'placeholder': "Your Comment",
            'id': 'exampleFormControlTextarea1',
            'rows': '3',
        }
    ))
