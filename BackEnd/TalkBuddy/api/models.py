from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save


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
    verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'mobileNumber'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.mobileNumber)

    def profile(self):
        profile = profile.objects.get(user=self)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    bio = models.CharField(max_length=250)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    email = models.EmailField()
    emailVerified = models.BooleanField(default=False)
    fullName = models.CharField(max_length=300)

    def fullName(self):
        return f"{self.firstName} {self.lastName}"

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

