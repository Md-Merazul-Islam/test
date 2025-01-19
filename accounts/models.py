from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
   
    ADMIN = 'Admin'
    TRAINER = 'Trainer'
    TRAINEE = 'Trainee'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (TRAINER, 'Trainer'),
        (TRAINEE, 'Trainee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=TRAINEE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)