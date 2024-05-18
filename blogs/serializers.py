from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Blog, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class BlogSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        request = self.context["request"]
        if request and hasattr(request, "user"):
            return obj.likes.filter(user=request.user).exists()
        return False

    class Meta:
        model = Blog
        fields = ["id", "title", "content", "created_at", "author", "tagline", "num_likes", "is_liked"]
        read_only_fields = ["author", "num_likes", "is_liked"]



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "blog", "text", "created_at"]
        extra_kwargs = {"author": {"read_only": True}, "blog": {"read_only": True}}
