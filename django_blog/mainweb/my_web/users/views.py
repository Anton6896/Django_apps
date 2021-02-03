from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (UserRegisterForm, ProfileUpdateForm, UserUpdateForm)
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            # log in user
            user = authenticate(username=username,
                                password=form.cleaned_data.get('password1'))
            if user:  # check the valid user before login
                if user.is_active:
                    login(request, user)

            messages.success(request, f'account created for {username}')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'register'})


@login_required
def profile_user(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            pic_name = profile_update_form.cleaned_data['image']
            profile_update_form.save()
            
            # change the name of the file that user saved 

            messages.success(request, f' tnx {request.user.username}, your data has been updated')
            return redirect('users-profile')

    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'profile',
        'u_form': user_update_form,
        'p_form': profile_update_form
    }

    return render(request, 'users/profile.html', context)


def about(request):
    context = {
        'title': 'About page'
    }
    return render(request, 'users/about.html', context)
