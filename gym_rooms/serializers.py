from rest_framework import serializers
from .models import User, Trainee, Trainer, ClassSchedule,Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','role','phone_number','address']
        

class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Trainer
        fields = ['id', 'user']
        
class TraineeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Trainee
        fields = ['id', 'user',]

class ClassScheduleSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer()
    remaining_slots = serializers.SerializerMethodField()

    class Meta:
        model = ClassSchedule
        fields = ['id', 'date', 'start_time', 'end_time', 'trainer', 'max_trainees', 'remaining_slots']

    def get_remaining_slots(self, obj):
        return obj.max_trainees - obj.bookings.count()
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'trainee', 'schedule','booking_time']

