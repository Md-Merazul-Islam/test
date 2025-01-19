from django.urls import path
from .views import TrainerScheduleView

urlpatterns = [
    path('my-schedules/', TrainerScheduleView.as_view(), name='trainer-schedules'),
]
