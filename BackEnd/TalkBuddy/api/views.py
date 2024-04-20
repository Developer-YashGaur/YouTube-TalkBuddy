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
import jwt
from datetime import datetime
import environ



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
    
class TokenValidate(APIView):
    permission_classes = ([IsAuthenticated])
    

    def get(self, request):
        env = environ.Env()
        environ.Env.read_env()
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            # Remove 'Bearer ' prefix from the token
            token = token.split()[1]
            payload = jwt.decode(token, env("SECRET_KEY"), algorithms=['HS256'])
            expiration_time = datetime.fromtimestamp(payload['exp'])

            response_data = {
                'expired': datetime.now() > expiration_time,
                'expire_at': expiration_time.strftime('%Y-%m-%d %H:%M:%S')
            }

            return Response(response_data, status=200)

        except jwt.ExpiredSignatureError:
            return Response({'expired': True, 'expire_at': None}, status=200)

        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=401)
        