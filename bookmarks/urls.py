from django.urls import path
from .views import BookmarkPostView, ListBookmarksView

urlpatterns = [
    path('', ListBookmarksView.as_view(), name="list-bookmarks"),
    path('<int:post_id>/', BookmarkPostView.as_view(), name="bookmark-post"),
]
