from django.db import models
from accounts.models import User

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')




class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainee_profile')
    
    
    
class ClassSchedule(models.Model):
    date= models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, related_name='class_schedule')
    max_trainees = models.IntegerField(default=10)
    
    def __str__(self):
        return f"{self.date}  - {self.start_time} - {self.end_time} - {self.trainer.user.username}"
    
    
class Booking(models.Model):
    schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name="bookings")
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name="bookings")
    booking_time = models.DateTimeField(auto_now_add=True ,null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['schedule', 'trainee'], name='unique_schedule_trainee')
        ]

        
    
