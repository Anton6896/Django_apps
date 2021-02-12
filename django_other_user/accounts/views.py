from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RegisterForm


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:register")

    def form_valid(self, form):
        user = get_user_model()
        user.objects.create_user(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password2')
        )
        return super().form_valid(form)
