from django.urls import path
from .views import (
    SignupView,
    PersonnelLoginView,
    ComputeBMIView,
    AdminLoginView,
    AdminChangePasswordView,
    AdminForgotPasswordView,
    AdminVerifyOtpView,
    AdminPersonnelListView,
    AdminPersonnelDetailView,
    AdminPersonnelPasswordResetView,
    AdminLoginHistoryView,
    AdminExportView,
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('personnel/login/', PersonnelLoginView.as_view(), name='personnel-login'),
    path('personnel/compute/', ComputeBMIView.as_view(), name='compute-bmi'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/change-password/', AdminChangePasswordView.as_view(), name='admin-change-password'),
    path('admin/forgot-password/', AdminForgotPasswordView.as_view(), name='admin-forgot-password'),
    path('admin/verify-otp/', AdminVerifyOtpView.as_view(), name='admin-verify-otp'),
    path('admin/personnel/', AdminPersonnelListView.as_view(), name='admin-personnel-list'),
    path('admin/personnel/<int:pk>/', AdminPersonnelDetailView.as_view(), name='admin-personnel-detail'),
    path('admin/personnel/<int:pk>/reset-password/', AdminPersonnelPasswordResetView.as_view(), name='admin-personnel-reset-password'),
    path('admin/login-history/', AdminLoginHistoryView.as_view(), name='admin-login-history'),
    path('admin/export/', AdminExportView.as_view(), name='admin-export'),
]
