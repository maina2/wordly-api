from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture', 'website')
        read_only_fields=('id',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'bio', 'profile_picture', 'website')
        
    def create(self, validated_data):
        # Create the user with the password field
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user