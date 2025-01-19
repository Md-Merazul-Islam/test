from django.urls import path
from .views import BookingView

urlpatterns = [
    path('bookings/', BookingView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingView.as_view(), name='booking-detail'),
]
