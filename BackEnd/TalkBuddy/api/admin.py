from django.contrib import admin
from api.models import User, Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['mobileNumber']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'emailVerified', 'fullName']


admin.site.register(User)
admin.site.register(Profile)