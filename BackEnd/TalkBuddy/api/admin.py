from django.contrib import admin
from api.models import User, Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    # list_editable = ['verified']
    list_display = ['id','mobileNumber', 'fullName', 'createdAt', 'updatedAt', 'verified']
    exclude = ['email']
    ordering = ['id']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'createdAt', 'updatedAt', 'emailVerified']
    ordering = ['id']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)