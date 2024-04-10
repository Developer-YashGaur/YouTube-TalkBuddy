from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import User
from phonenumber_field.phonenumber import PhoneNumber
from .utils import generate_otp, send_otp_phone
from django.utils import timezone


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    mobileNumber = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('mobileNumber', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            password = "Password fields didn't match."
            raise serializers.ValidationError({"password": password})

        return attrs

    def create(self, validated_data):
        otp = generate_otp()
        otp_generation_time = timezone.now()
        user = User.objects.create(
            mobileNumber = validated_data['mobileNumber'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            otp = otp,
            otpGenerationTime = otp_generation_time
        )

        user.set_password(validated_data['password'])
        user.save()
        send_otp_phone(validated_data['mobileNumber'], otp)


        return user
    
class UserExistSerializer(serializers.Serializer):
    mobileNumber = serializers.CharField()

    def validate_mobileNumber(self, value):
        try:
            number = PhoneNumber.from_string(value)
            User.objects.get(mobileNumber=number.as_e164)
            return {'mobileNumber': f"{number}", 'exist': True}
        except User.DoesNotExist:
            return {'mobileNumber': f"{number}", 'exist': False}
        
    def create(self, validated_data):
        return validated_data
    
    def to_representation(self, instance):
        return {
            'mobileNumber': instance['mobileNumber']['mobileNumber'],
            'exist': instance['mobileNumber']['exist']
        }
    

class ValidateOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    mobileNumber = serializers.CharField()


    def validate(self, attrs):
        try:
            otp = attrs['otp']
            number = PhoneNumber.from_string(attrs['mobileNumber'])
            user = User.objects.get(mobileNumber=number.as_e164)
        
        except User.DoesNotExist:
            return {'error': 'User with this mobile number does not exist.', 'validated': False}

        if (timezone.now() - user.otpGenerationTime).total_seconds() <= 60: 
            if user.otp == otp:
                user.otp = None  # Reset the OTP field after successful validation
                user.verified = True
                token = MyTokenObtainPairSerializer.get_token(user)
                user.save()

                return {'message': "Mobile number is successfully verified", 'validated': True, 'token': str(token.access_token)}
            else:
                return {'error': 'Invalid OTP.', 'validated': False}
        else:
                user.otp = None
                user.verified = False
                user.save()
                return {'error': 'OTP Time has expired', 'validated': False}
        
    def create(self, validated_data):
        return validated_data

    def to_representation(self, instance):
        return instance
    
class ResendOTPSerializer(serializers.Serializer):
    mobileNumber = serializers.CharField()

    def validate(self, value):
        try:
            number = PhoneNumber.from_string(value['mobileNumber'])
            user = User.objects.get(mobileNumber=number.as_e164)
        
        except User.DoesNotExist:
            return {'error': 'User with this mobile number does not exist.', 'validated': False}
        
        otp = generate_otp()
        otp_generation_time = timezone.now()
        user.otp = otp
        user.otpGenerationTime = otp_generation_time
        user.save()
        send_otp_phone(number, otp)
        return {'message': 'OTP successfully send'}

    def create(self, validated_data):
        return validated_data
    
    def to_representation(self, instance):
        return instance
    
class ForgotPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            password = "Password field didn't watch."
            raise serializers.ValidationError({"password": password})
        return attrs
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
    def create(self, validated_data):
        return validated_data
    
    def to_representation(self, instance):
        return instance
        
