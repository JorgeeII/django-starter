from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None,
            {'fields': ('username', 'password')}),
        ('Personal info',
            {'fields': ('first_name', 'last_name', 'email', 'age')}),
        ('Permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        ('Important dates',
            {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(models.CustomUser, CustomUserAdmin)
