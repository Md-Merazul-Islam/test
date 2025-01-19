from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from admins.models import ClassSchedule, Trainer
from admins.serializers import ClassScheduleSerializer

class TrainerScheduleView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassScheduleSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            trainer = Trainer.objects.get(username=user.username)
        except Trainer.DoesNotExist:
            raise ValueError("Trainer not found")

        queryset = ClassSchedule.objects.filter(trainer=trainer).order_by('date', 'start_time')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()


            if not queryset.exists():
                return Response(
                    {
                        "success": False,
                        "message": "No schedule found.",
                        "errorDetails": {
                            "field": "trainer",
                            "message": "No classes associated with the logged-in trainer."
                        },
                    },
                    status=status.HTTP_404_NOT_FOUND
                )


            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "success": True,
                    "statusCode": 200,
                    "message": "Schedules fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK
            )

        except ValueError as error:
            return Response(
                {
                    "success": False,
                    "message": "Validation error occurred. Check your macked trainer name and gmail address are right plz.",
                    "errorDetails": {
                        "field": "trainer",
                        "message": str(error),
                    },
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as error:
            return Response(
                {
                    "success": False,
                    "message": "An error occurred while fetching the schedules.",
                    "errorDetails": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
