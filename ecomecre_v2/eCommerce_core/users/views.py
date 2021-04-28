from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import LogInForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.utils.http import is_safe_url
from django.views.generic.edit import FormView
from .signals import user_logged_in


def home_page(request):
    """
    past data from cart view to this view
    session variable
    """
    # name = request.session.get("name", "unknown")  # getter
    # print(f"data from card (name) ======= {name}")
    # request.session["cart_total"] = cart.get_amount()

    return render(request, 'home_page.html')


class RegisterView(FormView):
    template_name = 'register_user.html'
    form_class = RegisterForm
    success_url = reverse_lazy("users:login_page")

    def form_valid(self, form):
        user = get_user_model()
        user.objects.create_user(
            username=form.cleaned_data.get('username'),
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password')
        )
        messages.success(self.request, f'welcome:  {form.cleaned_data.get("username")} was created')
        return super().form_valid(form)


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        user = get_user_model()

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user.objects.create_user(
                username, email, password
            )

            messages.success(request, f'wellcom {username} was created')
            return redirect("users:login_page")
    else:
        form = RegisterForm()

    return render(request, "register_user.html", {"form": form})


def login_user(request):
    form = LogInForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        if user is not None:
            login(request, user)

            # send signal at user log in
            user_logged_in.send(user.__class__, instance=user, request=request)

            messages.success(request, f'welcome {username}')
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            return redirect("users:home_page")

        else:
            pass
            # do nothing

    return render(request, "login.html", {"form": form})


def profile_edit(request): pass


# todo profile manipulation , password change, pic change etc


def bootstrap_page(request):
    form = LogInForm(request.POST or None)

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post

        if user is not None:
            login(request, user)

            messages.success(request, f'welcome {username}')
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            return redirect("users:home_page")

        else:
            pass
            # do nothing

    return render(request, 'bootstrap/home.html', {"form": form})
