# from rest_framework import serializers
# from .models import Booking
# from accounts.serializers import UserDetailSerializer

# class BookingSerializer(serializers.ModelSerializer):
#     trainee = UserDetailSerializer(read_only=True)
#     # schedule = serializers.SerializerMethodField()

#     class Meta:
#         model = Booking
#         fields = ['id', 'trainee', 'schedule', 'booking_time']
#         read_only_fields = ['trainee', 'booking_time']

#     def create(self, validated_data):
#         request = self.context.get('request')
#         if request and hasattr(request, 'user'):
#             validated_data['trainee'] = request.user
#         return super().create(validated_data)


from rest_framework import serializers
from .models import Booking
from accounts.serializers import UserDetailSerializer
from admins.models import ClassSchedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = ['date', 'start_time', 'end_time', 'current_trainees']  # Adjust fields as per your Schedule model

class BookingSerializer(serializers.ModelSerializer):
    trainee = UserDetailSerializer(read_only=True)
    schedule_info = ScheduleSerializer(source='schedule', read_only=True)  # Nested serializer for GET requests

    class Meta:
        model = Booking
        fields = ['id', 'trainee', 'schedule', 'schedule_info', 'booking_time']
        read_only_fields = ['trainee', 'booking_time']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['trainee'] = request.user
        return super().create(validated_data)
