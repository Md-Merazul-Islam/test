# from django.urls import path
# from .views import TrainerView, TrainerDetailView, TrainerScheduleView

# urlpatterns = [
#     path('trainers-list/', TrainerView.as_view(), name='trainer-list'),  # List all trainers & create trainer
#     path('trainers/<int:trainer_id>/', TrainerDetailView.as_view(), name='trainer-detail'),  # Update & delete trainer
#     path('my-trainer-schedules/', TrainerScheduleView.as_view(), name='trainer-schedule-list'),  # Fetch trainer schedules
# ]




from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainerViewSet, ClassScheduleViewSet

router = DefaultRouter()
router.register(r'trainers', TrainerViewSet, basename='trainer')
router.register(r'class-schedules', ClassScheduleViewSet, basename='class-schedule')

urlpatterns = [
    path('', include(router.urls)),
]
