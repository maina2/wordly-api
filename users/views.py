from django.contrib.auth import get_user_model, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

# User Registration (Open to anyone)
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Anyone can register

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)  # Generate JWT tokens
            response = {
                "message": "User registered successfully",
                "data": serializer.data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login (Open to anyone)
class LoginView(APIView):
    permission_classes = [AllowAny]  # Anyone can log in

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            response = {
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            }
            return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(data={"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Protected Route: Get & Update User Profile (Requires Authentication)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can access

    def get(self, request, *args, **kwargs):
        user = request.user  # Authenticated user
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Received logout request with data:", request.data)  # Debugging

        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklists the token (if enabled)
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

