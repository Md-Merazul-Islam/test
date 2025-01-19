from django.db import models
from accounts.models import User
from datetime import datetime, timedelta
from django.db import models

class Trainer(models.Model):
    username = models.CharField(max_length=100, unique=True ,null=True, blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)

    def __str__(self):
        return self.username
    

class ClassSchedule(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, related_name='class_schedules')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    max_trainees = models.IntegerField(default=10)

    def save(self, *args, **kwargs):
        if not self.end_time:
            start_datetime = datetime.combine(self.date, self.start_time)
            self.end_time = (start_datetime + timedelta(hours=2)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.start_time} - {self.trainer.username if self.trainer else 'No Trainer'}"
