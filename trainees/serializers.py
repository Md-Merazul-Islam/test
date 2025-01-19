from rest_framework import serializers
from .models import Booking
from accounts.serializers import UserDetailSerializer

class BookingSerializer(serializers.ModelSerializer):
    trainee = UserDetailSerializer(read_only=True)
    schedule = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'trainee', 'schedule', 'booking_time']
        read_only_fields = ['trainee', 'booking_time']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['trainee'] = request.user
        return super().create(validated_data)

    def get_schedule(self, obj):
        schedule = obj.schedule
        return {
            "date": schedule.date,
            "start_time": schedule.start_time,
            "end_time": schedule.end_time,
            "current_trainees": schedule.current_trainees
        }
