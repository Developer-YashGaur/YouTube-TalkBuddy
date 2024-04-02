from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import User
from phonenumber_field.phonenumber import PhoneNumber

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    mobileNumber = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('mobileNumber', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            password = "Password fields didn't match."
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            mobileNumber = validated_data['mobileNumber'],
        )

        user.set_password(validated_data['password'])
        user.save()

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