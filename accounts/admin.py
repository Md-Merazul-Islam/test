from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):

    model = User
    list_display = ( 'id','username', 'email', 'role', 'phone_number', 'address', 'is_staff', 'is_active')  
    list_filter = ('role', 'is_staff', 'is_active')  
    search_fields = ('username', 'email', 'role')  
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone_number', 'address')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone_number', 'address')}),
    )

admin.site.register(User, CustomUserAdmin)
