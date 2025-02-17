from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Bookmark
from posts.models import Post
from .serializers import BookmarkSerializer

class BookmarkPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)

        if created:
            return Response({"message": "Post bookmarked successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Post already bookmarked"}, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        try:
            bookmark = Bookmark.objects.get(user=request.user, post_id=post_id)
            bookmark.delete()
            return Response({"message": "Bookmark removed"}, status=status.HTTP_204_NO_CONTENT)
        except Bookmark.DoesNotExist:
            return Response({"error": "Bookmark not found"}, status=status.HTTP_404_NOT_FOUND)


class ListBookmarksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookmarks = Bookmark.objects.filter(user=request.user)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
