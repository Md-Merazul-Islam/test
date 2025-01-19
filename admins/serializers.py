from rest_framework import serializers
from .models import Trainer, ClassSchedule
from datetime import datetime, timedelta
class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ['id', 'username', 'email']


class ClassScheduleSerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(source='trainer.username', read_only=True)

    class Meta:
        model = ClassSchedule
        fields = ['id', 'date', 'start_time', 'end_time', 'trainer', 'trainer_name','current_trainees']
        read_only_fields = ['end_time', 'current_trainees']   

    def create(self, validated_data):
        start_time = validated_data.get("start_time")

        if start_time:
            start_datetime = datetime.combine(validated_data["date"], start_time)
            validated_data["end_time"] = (start_datetime + timedelta(hours=2)).time()

        return super().create(validated_data)
