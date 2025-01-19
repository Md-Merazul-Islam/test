# Generated by Django 5.1.5 on 2025-01-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.UniqueConstraint(fields=('schedule', 'trainee'), name='unique_schedule_trainee'),
        ),
    ]
