from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from datetime import timedelta
from .permissions import IsAdmin, IsTrainer, IsTrainee
from .serializers import ClassScheduleSerializer, BookingSerializer
from .models import ClassSchedule, Booking
from rest_framework.response import Response


# Response helpers
def success_response(message, data=None, status_code=200):
    response = {
        "success": True,
        "statusCode": status_code,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return Response(response, status=status_code)


def error_response(message, error_details=None, status_code=400):
    response = {
        "success": False,
        "message": message,
    }
    if error_details is not None:
        response["errorDetails"] = error_details
    return Response(response, status=status_code)


# Views
class CLassScheduleView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & IsAdmin]
    serializer_class = ClassScheduleSerializer

    def get_queryset(self):
        return ClassSchedule.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            date = request.data.get('date')
            start_time = request.data.get('start_time')
            end_time = request.data.get('end_time')

            if not date or not start_time or not end_time:
                return error_response("Date, start time, and end time are required.", status_code=400)

            if timedelta(hours=2) != timedelta(hours=int(end_time.split(':')[0]) - int(start_time.split(':')[0])):
                return error_response("Class duration should be 2 hours.", status_code=400)

            daily_schedules = ClassSchedule.objects.filter(date=date).count()
            if daily_schedules >= 5:
                return error_response("Maximum daily 5 schedules allowed.", status_code=400)
            return super().create(request, *args, **kwargs)
        except Exception as error:
            return error_response("An error occurred while creating.", error_details=str(error), status_code=500)


class BookingView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated & IsTrainee]
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        try:
            schedule_id = request.data.get('schedule')
            if not schedule_id:
                return error_response("Schedule ID is required.", status_code=400)
            schedule = ClassSchedule.objects.get(id=schedule_id)

            if Booking.objects.filter(
                trainee=request.user.trainee_profile,
                schedule__start_time=schedule.start_time,
                schedule__date=schedule.date
            ).exists():
                return error_response("You have already booked this class. You cannot book multiple classes in the same time slot.",
                    status_code=400,)

            if schedule.bookings.count() >= schedule.max_trainees:
                return error_response("Sorry, Class schedule is full. Maximum 10 trainees allowed per schedule.",
                    status_code=400,)

            booking = super().create(request, *args, **kwargs)
            return success_response("You have successfully booked this class. Thank you.",
                data=BookingSerializer(booking.instance).data,
                status_code=201,
            )
        except ClassSchedule.DoesNotExist:
            return error_response("Class schedule not found.", status_code=404)
        except Exception as error:
            return error_response("An error occurred while booking the class.", error_details=str(error), status_code=500)


class TrainerSchedulerView(generics.ListAPIView):
    permission_classes = [IsAuthenticated & (IsTrainer | IsAdmin)]
    serializer_class = ClassScheduleSerializer

    def get_queryset(self):
        return ClassSchedule.objects.filter(trainer=self.request.user.trainer_profile)


class BookingCancelView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated & IsTrainee]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  
            return Booking.objects.none()
        return Booking.objects.filter(trainee=self.request.user.trainee_profile)

    def delete(self, request, *args, **kwargs):
        try:
            booking_id = kwargs.get('pk')
            booking = Booking.objects.filter(id=booking_id, trainee=request.user.trainee_profile).first()
            if not booking:
                return error_response("Booking not found.", status_code=404)

            booking.delete()
            return success_response("Booking successfully canceled.", status_code=204)
        except Exception as error:
            return error_response("An error occurred while canceling the booking.", error_details=str(error), status_code=500)
