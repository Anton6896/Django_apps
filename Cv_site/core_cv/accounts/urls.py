from django.urls import path
from . import views as acc_views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    # basic web 
    path('', acc_views.HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('register/', acc_views.MyRegisterView.as_view(), name='register'),


    # api calls
    path('api/committee_create/', acc_views.CommitteeUserCreationView.as_view()),
    path('api/tenant_create/', acc_views.TenantUserCreationView.as_view()),
    path('api/tetant_list/', acc_views.TenantsListView.as_view()),
    path('api/tetant_detail/<int:pk>/', acc_views.TenantDetailView.as_view()),

]

#  http://127.0.0.1:8000/auth-token/token/login/
#  http://127.0.0.1:8000/auth-token/token/logout/

# http://127.0.0.1:8000/api/tenant_create/
# http://127.0.0.1:8000/api/committee_create/
# http://127.0.0.1:8000/api/tetant_list/
# http://127.0.0.1:8000/api/tetant_detail/  ?=pk
