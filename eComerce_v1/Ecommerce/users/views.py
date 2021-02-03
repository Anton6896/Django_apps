from django.shortcuts import render, redirect
from django.views import generic
from . import forms
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.


class MyRegisterForm(generic.View):

    def get(self, *args, **kwarg):
        form = forms.MyUserRegisterForm()

        context = {
            'title': 'register',
            'form': form
        }

        return render(self.request, 'register_form.html', context)

    def post(self, *arg, **kwarg):
        form = forms.MyUserRegisterForm(self.request.POST)

        if form.is_valid():
            form.save()

            # log in user
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password1'))
            if user:  # check the valid user before login
                if user.is_active:
                    login(self.request, user)

            messages.success(self.request, 'you are was registred')
            return redirect('/')

        