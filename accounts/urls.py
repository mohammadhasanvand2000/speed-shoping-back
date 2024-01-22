# accounts/urls.py

from django.urls import path
from .views import RegisterView
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('request-reset-email', views.RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password_reset_confrim'),
    path('reset_password_complate/<uidb64>/<token>/', views.SetNewPasswordAPI.as_view(), name='reset_password_complate'),
]
