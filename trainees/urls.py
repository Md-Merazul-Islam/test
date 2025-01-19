from django.urls import path
from .views import BookingView,BookingDetailView

urlpatterns = [
    path('bookings/', BookingView.as_view(), name='booking-list'),
    path('bookingss/<int:pk>/', BookingView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
]


# for booking json input 
# {
#     "schedule": 1
# }
