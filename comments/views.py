from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment
from .serializers import CommentSerializer
from django.shortcuts import get_object_or_404
from posts.models import Post

class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id).order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)  # ✅ Get the post instance
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)  # ✅ Assign post here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, comment_id):
        return Comment.objects.get(id=comment_id)

    def get(self, request, comment_id):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, comment_id):
        comment = self.get_object(comment_id)
        if request.user != comment.author:
            return Response({"error": "You can only edit your own comments"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)
        if request.user != comment.author:
            return Response({"error": "You can only delete your own comments"}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
