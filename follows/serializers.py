from rest_framework import serializers
from .models import Follow
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()
    following = serializers.StringRelatedField()

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
