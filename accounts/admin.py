from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'id', 'email', 'phone_number', 'address', 'role', 'is_staff', 'is_active')  # Add 'role'
    list_filter = ('role', 'is_staff', 'is_active')  # Add 'role' filter
    search_fields = ('username', 'email')  
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'address', 'role')}),  # Add 'role' here
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'address', 'role')}),  # Add 'role' here
    )

admin.site.register(User, CustomUserAdmin)
