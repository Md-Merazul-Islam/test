# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.utils.timezone import now, timedelta
# from admins.models import ClassSchedule
# from .serializers import TrainerScheduleSerializer
# from rest_framework.permissions import IsAuthenticated
# from .permissions import IsAdmin
# from admins.models import Trainer
# from admins.serializers import TrainerSerializer


# def success_response(message, data=None, status_code=200):
#     response = {
#         "success": True,
#         "statusCode": status_code,
#         "message": message,
#     }
#     if data is not None:
#         response["data"] = data
#     return Response(response, status=status_code)


# def error_response(message, error_details=None, status_code=400):
#     response = {
#         "success": False,
#         "message": message,
#     }
#     if error_details is not None:
#         response["errorDetails"] = error_details
#     return Response(response, status=status_code)


# class TrainerView(APIView):
#     permission_classes = [IsAuthenticated, IsAdmin]
    
#     def get(self, request):
#         trainers = Trainer.objects.all()
#         serializer = TrainerSerializer(trainers, many=True)
#         return success_response("Trainer list fetched successfully.", serializer.data)
    
#     def post(self, request):
#         serializer = TrainerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return success_response("Trainer created successfully.", serializer.data, status_code=201)
#         return error_response("Failed to create trainer.", serializer.errors)
    
    
# class TrainerDetailView(APIView):
#     permission_classes = [IsAuthenticated, IsAdmin]

#     def put(self, request, trainer_id):
#         try:
#             trainer = Trainer.objects.get(id=trainer_id)
#             serializer = TrainerSerializer(trainer, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return success_response("Trainer updated successfully.", serializer.data)
#             return error_response("Failed to update trainer.", serializer.errors)
#         except Trainer.DoesNotExist:
#             return error_response("Trainer not found.", status_code=404)

#     def delete(self, request, trainer_id):
#         try:
#             trainer = Trainer.objects.get(id=trainer_id)
#             trainer.delete()
#             return success_response("Trainer deleted successfully.")
#         except Trainer.DoesNotExist:
#             return error_response("Trainer not found.", status_code=404)


# class TrainerScheduleView(APIView):
#     permission_classes = [IsAuthenticated | IsAdmin]

#     def get(self, request):
#         try:
#             # Fetch trainer schedules
#             trainer = request.user.trainer
#             schedules = ClassSchedule.objects.filter(trainer=trainer).order_by('date', 'start_time')

#             # Group schedules by week
#             weekly_schedules = {}
#             for schedule in schedules:
#                 week_start = (schedule.date - timedelta(days=schedule.date.weekday())).strftime('%Y-%m-%d')
#                 if week_start not in weekly_schedules:
#                     weekly_schedules[week_start] = []
#                 weekly_schedules[week_start].append(schedule)

#             # Serialize grouped data
#             serialized_data = {
#                 week: TrainerScheduleSerializer(week_schedules, many=True).data
#                 for week, week_schedules in weekly_schedules.items()
#             }

#             return Response({
#                 "success": True,
#                 "message": "Trainer schedules fetched successfully.",
#                 "data": serialized_data
#             })
#         except Exception as e:
#             return Response({
#                 "success": False,
#                 "message": "Failed to fetch trainer schedules.",
#                 "error": str(e)
#             }, status=400)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from admins.models import ClassSchedule
from admins.serializers import  ClassScheduleSerializer 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin
from admins.models import Trainer
from admins.serializers import TrainerSerializer
from rest_framework import viewsets


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request, *args, **kwargs):
        """
        Fetch all trainers and return trainer choices for dropdown selection.
        """
        trainers = Trainer.objects.all()
        serializer = self.get_serializer(trainers, many=True)

        # Generate dropdown choices
        trainer_choices = [{"id": trainer.id, "name": trainer.user.username} for trainer in trainers]

        return Response({
            "success": True,
            "message": "Trainer list fetched successfully.",
            "trainers": serializer.data,
            "trainer_choices": trainer_choices  # Dropdown selection data
        })

class ClassScheduleViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        """
        Validate and create a class schedule.
        """
        trainer_id = request.data.get('trainer')
        if not Trainer.objects.filter(id=trainer_id).exists():
            return Response({"success": False, "message": "Invalid trainer selection."}, status=400)

        return super().create(request, *args, **kwargs)
