from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):

    model = User
    list_display = ( 'username','id', 'email', 'phone_number', 'address', 'is_staff', 'is_active')  
    list_filter = ( 'is_staff', 'is_active')  
    search_fields = ('username', 'email', 'role')  
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ( 'phone_number', 'address')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ( 'phone_number', 'address')}),
    )

admin.site.register(User, CustomUserAdmin)
