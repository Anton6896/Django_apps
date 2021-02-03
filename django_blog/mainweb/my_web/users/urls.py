from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


# app_name = 'users_app'

urlpatterns = [
    path('register/', views.register, name='users-register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),
         name='users-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='users-logout'),
    path('profile', views.profile_user, name='users-profile'),
    path('about/', views.about, name='users-about'),
    # password reset feature
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
         template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name='users/password_reset_complete.html'), name='password_reset_complete'),


]
