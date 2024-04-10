from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import MyTokenObtainPairView, RegisterView, UserExist, ValidateOTP, ResendOTP, LogoutView, ForgotPassword

urlpatterns = [
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('login', MyTokenObtainPairView.as_view(), name="login"),
    path('register', RegisterView.as_view(), name="register"),
    path('userExist', UserExist.as_view(), name="userExist"),
    path('validateAPI', ValidateOTP.as_view(), name="validateOtp"),
    path('resendOTP', ResendOTP.as_view(), name="resendOTP"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('forgotPassword', ForgotPassword.as_view(), name="forgotPassword")
]