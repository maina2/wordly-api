from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Like
from posts.models import Post
from .serializers import LikeSerializer

class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()  # Unlike if already liked
            return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)
        
        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)
