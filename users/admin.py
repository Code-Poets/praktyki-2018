from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.forms.form_custom_user_creation import CustomUserCreationForm
from users.forms.form_custom_user_change import  CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'nick', 'email', 'date_joined', 'updatedat', 'last_login']
    list_filter = ('date_joined',)
    #fieldsets = (
    #        ('User Profile', {'fields': ('nick','email')}),
    #) + AuthUserAdmin.fieldsets
    fieldsets = (
        ('Change user', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('nick', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined', 'last_login', 'updatedat')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
