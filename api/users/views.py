from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample

User = get_user_model()



@extend_schema(
    description="Create a new user account",
    request=UserSerializer,
    responses={
        201: UserSerializer,
    },
    examples=[
        OpenApiExample(
            'Example User Creation',
            summary='Create a user example',
            description='An example of a request to create a new user.',
            value={
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'password': 'password123',
            },
        ),
    ],
)
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@extend_schema(
    description="Obtain a JWT token pair for authentication",
    request=CustomTokenObtainPairSerializer,
    responses={200: CustomTokenObtainPairSerializer},
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
