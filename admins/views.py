from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from rest_framework.response import Response
from .models import ClassSchedule, Trainer
from .serializers import ClassScheduleSerializer, TrainerSerializer
from .permissions import IsAdmin

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


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get("name")
            email = request.data.get("email")  
            username = request.data.get("username")  
            expertise = request.data.get("expertise")

            if not name or not email or not username or not expertise:
                return error_response(
                    "Name, email, username, and expertise are required fields.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if Trainer.objects.filter(username=username).exists():
                return error_response(
                    "Username already exists.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if Trainer.objects.filter(email=email).exists():
                return error_response(
                    "Email already exists.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            trainer = Trainer.objects.create(
                name=name,
                email=email,
                username=username,
                expertise=expertise
            )

            return success_response(
                "Trainer created successfully.",
                data=TrainerSerializer(trainer).data,
                status_code=status.HTTP_201_CREATED
            )

        except Exception as error:
            return error_response(
                "An error occurred while creating the trainer.",
                error_details=str(error),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            trainer = self.get_object()
            email = request.data.get("email")
            username = request.data.get("username")
            if not email or not username:
                return error_response(
                    "Name, email, username, and expertise are required fields.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if Trainer.objects.filter(username=username).exclude(id=trainer.id).exists():
                return error_response(
                    "Username already exists.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if Trainer.objects.filter(email=email).exclude(id=trainer.id).exists():
                return error_response(
                    "Email already exists.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            trainer.email = email
            trainer.username = username
            trainer.save()

            return success_response(
                "Trainer updated successfully.",
                data=TrainerSerializer(trainer).data,
                status_code=status.HTTP_200_OK
            )

        except Exception as error:
            return error_response(
                "An error occurred while updating the trainer.",
                error_details=str(error),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        try:
            trainer = self.get_object()
            trainer.delete()

            return success_response(
                "Trainer deleted successfully.",
                status_code=status.HTTP_204_NO_CONTENT
            )

        except Exception as error:
            return error_response(
                "An error occurred while deleting the trainer.",
                error_details=str(error),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClassScheduleView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ClassScheduleSerializer

    def get_queryset(self):
        return ClassSchedule.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            date = request.data.get("date")
            start_time = request.data.get("start_time")
            trainer_id = request.data.get("trainer")

            if not date or not start_time or not trainer_id:
                return error_response(
                    "Date, start time, and trainer are required.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            try:
                trainer = Trainer.objects.get(id=trainer_id)
            except Trainer.DoesNotExist:
                return error_response(
                    "Trainer not found.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            start_time_obj = datetime.strptime(start_time, "%H:%M").time()

            now = datetime.now()
            start_datetime = datetime.combine(now.date(), start_time_obj)

            # if start_datetime < now:
            #     return error_response(
            #         "Start time cannot be in the past.",
            #         status_code=status.HTTP_400_BAD_REQUEST
            #     )

            if ClassSchedule.objects.filter(date=date, start_time=start_time_obj, trainer=trainer).exists():
                return error_response(
                    "A class with the same trainer at this time and date already exists.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Limit to a maximum of 5 classes per day
            if ClassSchedule.objects.filter(date=date).count() >= 5:
                return error_response(
                    "Maximum of 5 classes can be scheduled for this day.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            end_time = (start_datetime + timedelta(hours=2)).time()

            overlapping_schedules = ClassSchedule.objects.filter(
                date=date,
                trainer=trainer,
                start_time__lt=end_time,
                end_time__gt=start_time_obj
            )

            if overlapping_schedules.exists():
                return error_response(
                    "Trainer has a conflicting class schedule at this time.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            class_schedule = ClassSchedule.objects.create(
                date=date,
                start_time=start_time_obj,
                end_time=end_time,
                trainer=trainer,
            )

            return success_response(
                "Class schedule created successfully.",
                data=ClassScheduleSerializer(class_schedule).data,
                status_code=status.HTTP_201_CREATED
            )

        except Exception as error:
            return error_response(
                "An error occurred while creating the class schedule.",
                error_details=str(error),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
