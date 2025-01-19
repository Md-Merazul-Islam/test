from django.db import models
from accounts.models import User
from datetime import timedelta
from admins.models import ClassSchedule


class Booking(models.Model):
    schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name="bookings")
    trainee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    booking_time = models.DateTimeField(auto_now_add=True ,null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['schedule', 'trainee'], name='unique_schedule_trainee')
        ]

        
    
