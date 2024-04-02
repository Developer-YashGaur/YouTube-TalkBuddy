from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import MyTokenObtainPairView, RegisterView, UserExist

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('login/', MyTokenObtainPairView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('userExist/', UserExist.as_view(), name="userExist")
]