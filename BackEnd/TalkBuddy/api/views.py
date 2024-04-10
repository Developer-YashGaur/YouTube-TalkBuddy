from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import MyTokenObtainPairSerializer, RegisterSerializer, UserExistSerializer, ValidateOTPSerializer, ResendOTPSerializer, ForgotPasswordSerializer
from rest_framework.throttling import AnonRateThrottle
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    throttle_classes = (AnonRateThrottle,)
    
class UserExist(APIView):
    def post(self, request):
        serializer = UserExistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
    
class ValidateOTP(APIView):
    def post(self, request):
        serializer = ValidateOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
    
class ResendOTP(APIView):
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class ForgotPassword(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            try:
                refresh_token = request.data["refresh_token"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(serializer.data, status.HTTP_200_OK)
            except:
                return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)