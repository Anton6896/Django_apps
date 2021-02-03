from rest_framework import generics, permissions
from . import serializers
from . import my_permissions
from . import models

from django.views.generic import View, UpdateView
from .forms import SighUpForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

user = get_user_model()

# regular html view     ====================================================================
class HomeView(View):
    def get(self, *args, **kwarg):
        return render(self.request, 'index.html')


class MyRegisterView(SuccessMessageMixin, View):

    def get(self, *args, **kwarg):
        form = SighUpForm()

        context = {
            'title': 'register',
            'form': form
        }

        return render(self.request, 'register.html', context)

    def post(self, *arg, **kwarg):
        form = SighUpForm(self.request.POST)

        context = {
            'title': 'register',
            'form': form
        }

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
        else:
            form = SighUpForm(self.request.POST)

        return render(self.request, 'register.html', context=context)


class UpdateProfileView(UpdateView):
    # todo user profile update / change form
    pass


#  api views            ====================================================================

class CommitteeUserCreationView(generics.CreateAPIView):
    # ! post_save add user to the group -> 'committee_group' for granting permissions #
    serializer_class = serializers.CommitteeSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(role='committee')


class TenantUserCreationView(generics.CreateAPIView):
    serializer_class = serializers.TenantSerializer
    # must have this for user identity search
    queryset = user.objects.all()

    permission_classes = [
        permissions.IsAuthenticated, my_permissions.IsCommettee
    ]

    def perform_create(self, serializer):
        serializer.save(role='tenant')


class TenantsListView(generics.ListAPIView):
    serializer_class = serializers.ListTenantsSerializer
    queryset = user.objects.filter(role='tenant').all()

    permission_classes = [
        permissions.IsAuthenticated, my_permissions.IsCommettee
    ]


class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ListTenantsSerializer
    queryset = user.objects.filter(role='tenant').all()
    permission_classes = [
        permissions.IsAuthenticated, my_permissions.IsCommettee
    ]
