from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ProfileAPIView, LogoutAPIView

# urlpatterns = [
#     path('register/', RegisterAPIView.as_view(), name='register'),
#     path('login/', LoginAPIView.as_view(), name='login'),
#     path('profile/', ProfileAPIView.as_view(), name='profile'),
#     path('logout/', LogoutAPIView.as_view(), name='logout'),


# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),


]
