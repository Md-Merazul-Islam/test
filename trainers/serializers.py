from rest_framework import serializers
from admins.models import ClassSchedule
class TrainerScheduleSerializer(serializers.ModelSerializer):
    trainer = ClassSchedule
    remaining_slots = serializers.SerializerMethodField()

    class Meta:
        model = ClassSchedule
        fields = ['id', 'date', 'start_time', 'trainer', 'max_trainees', 'remaining_slots']

    def get_remaining_slots(self, obj):
        return obj.max_trainees - obj.bookings.count()
        
