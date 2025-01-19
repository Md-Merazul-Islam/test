from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Booking
from .serializers import BookingSerializer

class BookingView(APIView):
    def get(self, request):
        # Fetch bookings for the logged-in trainee
        bookings = Booking.objects.filter(trainee=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            schedule = serializer.validated_data['schedule']

            # Check if trainee already has a booking for the same day
            existing_booking = Booking.objects.filter(
                trainee=request.user,
                schedule__date=schedule.date
            ).exists()
            if existing_booking:
                return Response(
                    {"success": False, "message": "You can only book one class per day."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if the class is already fully booked
            if schedule.current_trainees >= schedule.max_trainees:
                return Response(
                    {"success": False, "message": "Class is fully booked."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save booking and update the class's current_trainees count
            serializer.save(trainee=request.user)
            schedule.current_trainees += 1
            schedule.save()
            return Response(
                {"success": True, "message": "Booking successful.", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"success": False, "message": "Validation error occurred.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:
            # Fetch the booking
            booking = Booking.objects.get(pk=pk, trainee=request.user)

            # Decrement the trainee count in the schedule
            booking.schedule.current_trainees -= 1
            booking.schedule.save()

            # Delete the booking
            booking.delete()
            return Response(
                {"success": True, "message": "Booking cancelled successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Booking.DoesNotExist:
            return Response(
                {"success": False, "message": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND
            )
