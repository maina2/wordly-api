from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'image', 'created_at', 'updated_at')  # Exclude 'author'
        read_only_fields = ('id', 'created_at', 'updated_at')
