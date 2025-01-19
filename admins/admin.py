from django.contrib import admin
from .models import Trainer, ClassSchedule

class TrainerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')  
    search_fields = ('username', 'email')  
    list_filter = ('email',)  

class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'date', 'start_time', 'end_time', 'max_trainees')  
    search_fields = ('trainer__username', 'trainer__email', 'date')  
    list_filter = ('date', 'trainer')  
    
    def save_model(self, request, obj, form, change):
        if not obj.trainer:
            obj.trainer = None  
        super().save_model(request, obj, form, change)

admin.site.register(Trainer, TrainerAdmin)
admin.site.register(ClassSchedule, ClassScheduleAdmin)
