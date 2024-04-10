from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.utils import timezone


# Create your models here.
class CustomUserManager(UserManager):
    def create_user(self, mobileNumber, password=None, **extra_fields):
        if not mobileNumber:
            raise ValueError('The given mobile number must be set')
        user = self.model(mobileNumber=mobileNumber, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobileNumber, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(mobileNumber, password, **extra_fields)

class User(AbstractUser):
    mobileNumber = PhoneNumberField(null=False, blank=False, unique=True)
    username = models.CharField(unique=False, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otpGenerationTime = models.DateTimeField(blank=True)
    USERNAME_FIELD = 'mobileNumber'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.mobileNumber)

    def profile(self):
        profile = profile.objects.get(user=self)

    def fullName(self):
        return f"{self.first_name} {self.last_name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    bio = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to="user_images", default="default.jpg", blank=True)
    email = models.EmailField( blank=True)
    emailVerified = models.BooleanField(default=False)
    # fullName = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return str(self.user.mobileNumber)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

