from django.contrib import admin
from .models import Trainer, Trainee, ClassSchedule, Booking


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user',)  
    search_fields = ('user__username',)  

@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    list_display = ('user',)  
    search_fields = ('user__username',) 

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'trainer', 'max_trainees')  
    search_fields = ('trainer__user__username',)  
    list_filter = ('date', 'trainer')  


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'trainee', 'booking_time')  
    search_fields = ('schedule__trainer__user__username', 'trainee__user__username') 
    list_filter = ('schedule', 'trainee')  
