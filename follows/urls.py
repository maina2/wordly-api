from django.urls import path
from .views import FollowUserView, ListFollowersView, ListFollowingView

urlpatterns = [
    path('<str:username>/follow/', FollowUserView.as_view(), name="follow-user"),
    path('<str:username>/followers/', ListFollowersView.as_view(), name="list-followers"),
    path('<str:username>/following/', ListFollowingView.as_view(), name="list-following"),
]
