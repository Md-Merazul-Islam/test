from django.urls import path
from .views import CLassScheduleView, BookingView, TrainerSchedulerView, BookingCancelView

urlpatterns = [
    path('class-schedules/', CLassScheduleView.as_view(), name='class-schedule-list-create'),
    path('bookings/', BookingView.as_view(), name='booking-create'),
    path('trainer-schedules/', TrainerSchedulerView.as_view(), name='trainer-schedule-list'),
    path('bookings/<int:pk>/', BookingCancelView.as_view(), name='booking-cancel'),
]
