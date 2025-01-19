from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username