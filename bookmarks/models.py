from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarked_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate bookmarks

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"
