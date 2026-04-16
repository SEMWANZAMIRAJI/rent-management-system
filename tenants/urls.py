from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
app_name = "tenants"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('tenantslist', TenantListView.as_view(),name='list'),
    path('add/', TenantCreateView.as_view(),name='add'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # placeholder dashboard
    path('edit/<int:pk>/', TenantUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', TenantDeleteView.as_view(), name='delete'),
     # password reset
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='tenants/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='tenants/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='tenants/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='tenants/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]




