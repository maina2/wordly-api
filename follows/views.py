from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Follow
from django.contrib.auth import get_user_model
from .serializers import FollowSerializer

User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            user_to_follow = User.objects.get(username=username)
            if user_to_follow == request.user:
                return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

            follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

            if created:
                return Response({"message": f"You are now following {username}"}, status=status.HTTP_201_CREATED)
            return Response({"message": f"You are already following {username}"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, username):
        try:
            user_to_unfollow = User.objects.get(username=username)
            follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)

            if follow.exists():
                follow.delete()
                return Response({"message": f"You have unfollowed {username}"}, status=status.HTTP_200_OK)
            return Response({"error": f"You are not following {username}"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ListFollowersView(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            followers = user.followers.all()
            serializer = FollowSerializer(followers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ListFollowingView(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            following = user.following.all()
            serializer = FollowSerializer(following, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
