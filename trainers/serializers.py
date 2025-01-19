from rest_framework import serializers
from admins.models import ClassSchedule

class ClassScheduleSerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(source='trainer.username', read_only=True)

    class Meta:
        model = ClassSchedule
        fields = ['id', 'date', 'start_time', 'end_time', 'max_trainees', 'trainer_name']
