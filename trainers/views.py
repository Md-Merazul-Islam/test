from rest_framework import generics, permissions, status
from rest_framework.response import Response
from admins.models import ClassSchedule
from .serializers import ClassScheduleSerializer

class TrainerScheduleView(generics.ListAPIView):
    serializer_class = ClassScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]  
    def get_queryset(self):
        return ClassSchedule.objects.filter(trainer=self.request.user).order_by('date', 'start_time')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response(
                {"success": False, "message": "No class schedules found for this trainer."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "message": "Class schedules retrieved successfully.", "data": serializer.data}, 
            status=status.HTTP_200_OK
        )
