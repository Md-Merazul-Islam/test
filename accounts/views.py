from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserDetailSerializer, ChangeUserRoleSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from .permissions  import IsAdmin

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request):
        response = super().create(request)
        return Response({
            "success": True,
            "statusCode": status.HTTP_201_CREATED,
            "message": "Registration successful. You can now log in.",
            "data": response.data
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Validation error occurred.",
                "errorDetails": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        username_or_email = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = User.objects.filter(username=username_or_email).first(
        ) or User.objects.filter(email=username_or_email).first()
        if user:
            user = authenticate(
                request, username=user.username, password=password)
            if user:
                login(request, user)

                refresh = RefreshToken.for_user(user)
                return Response({
                    "success": True,
                    "statusCode": status.HTTP_200_OK,
                    "message": "Login successful.",
                    "data": {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user_id': user.id,
                        'username': user.username
                    }
                }, status=status.HTTP_200_OK)

            return Response({
                "success": False,
                "message": "Invalid credentials.",
                "errorDetails": "Please check your username or password."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": False,
            "message": "Invalid username or email.",
            "errorDetails": "User not found."
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response({
            "success": True,
            "statusCode": status.HTTP_200_OK,
            "message": "Profile retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            "success": True,
            "statusCode": status.HTTP_200_OK,
            "message": "Successfully logged out"
        }, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  

    def perform_update(self, serializer):
        user = serializer.instance
        if 'role' in serializer.validated_data and user.role != serializer.validated_data['role']:
            pass
        serializer.save()
