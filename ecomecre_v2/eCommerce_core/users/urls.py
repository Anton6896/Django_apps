from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path("", views.home_page, name="home_page"),  # <- main site cart_home page
    path("login/", views.login_user, name="login_page"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'),
         name='logout_page'),
    path("register/", views.register_user, name="register_page"),
    path("profile/", views.ProfilePage.as_view(), name="profile"),

    path("register_user/", views.RegisterView.as_view(), name="signup_user"),
    path("bootstrap/", views.bootstrap_page, name="bootstrap_page"),  # <- my own look at v5

]
