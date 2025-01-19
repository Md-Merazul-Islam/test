from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainerViewSet, ClassScheduleView

router = DefaultRouter()
router.register(r'trainers', TrainerViewSet)  

urlpatterns = [
    path("class-schedules/", ClassScheduleView.as_view(), name="class_schedule_list_create"),
    path("", include(router.urls)), 
]
