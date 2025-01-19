from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'trainee', 'schedule', 'booking_time']

    def validate(self, data):
        # Ensure trainee can only book one schedule per day
        schedule = data['schedule']
        trainee = self.context['request'].user

        if Booking.objects.filter(
            trainee=trainee, schedule__date=schedule.date
        ).exists():
            raise serializers.ValidationError("You can only book one class per day.")
        return data
