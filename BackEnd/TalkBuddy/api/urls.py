from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import MyTokenObtainPairView, RegisterView, UserExist, ValidateOTP, ResendOTP, LogoutView, ForgotPassword, TokenValidate

urlpatterns = [
    path('auth/token_refresh', TokenRefreshView.as_view(), name="token_refresh"), # Token Refresh
    path('auth/login', MyTokenObtainPairView.as_view(), name="login"), # User Login
    path('auth/register', RegisterView.as_view(), name="register"), # User Register
    path('auth/mobileNumberExist', UserExist.as_view(), name="mobileNumbeExist"),   # Mobile Number Exist
    path('auth/validateOTP', ValidateOTP.as_view(), name="validateOtp"),    # Validate OTP
    path('auth/generateOTP', ResendOTP.as_view(), name="generateOTP"),  # Generate OTP
    path('auth/logout', LogoutView.as_view(), name="logout"),   # User Logout
    path('auth/changePassword', ForgotPassword.as_view(), name="changetPassword"),   # Change Password
    path('auth/token_validate', TokenValidate.as_view(), name="token_validate"), # Token Expiry check
]