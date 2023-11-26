from rest_framework import serializers
from core_apps.blogs.models import BlogPost, BlogPostComment


class BlogPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostComment
        fields = "__all__"
        read_only_fields = ["owner"]


class BlogPostSerializer(serializers.ModelSerializer):
    comments = BlogPostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = "__all__"
        read_only_fields = ["owner"]
