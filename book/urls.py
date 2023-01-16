"account urls.py"
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterUserView, activate_view, DeleteUserView, ForgotPasswordView, NewPasswordView



urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('activate/<str:activation_code>/', activate_view),
    path('delete/<str:email>/', DeleteUserView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('password_confirm/<str:activation_code>', NewPasswordView.as_view()),
]