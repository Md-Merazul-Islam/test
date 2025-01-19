from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from admins.models import ClassSchedule
from .models import Booking
from .serializers import BookingSerializer

class BookingView(APIView):
    def get(self, request):
        bookings = Booking.objects.filter(trainee=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            schedule = serializer.validated_data['class_schedule']
            if schedule.current_trainees >= schedule.max_trainees:
                return Response({"error": "Class is fully booked."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            schedule.current_trainees += 1
            schedule.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        booking = Booking.objects.get(pk=pk, trainee=request.user)
        booking.class_schedule.current_trainees -= 1
        booking.class_schedule.save()
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
