from rest_framework import serializers

from core_apps.blogs.models import BlogPost, BlogPostComment


class BlogPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostComment
        fields = "__all__"
        read_only_fields = ["owner"]


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"
        read_only_fields = ["owner"]


class BlogPostSerializerWithComments(serializers.ModelSerializer):
    # comments is the related_name for the BlogPost foreign key in the BlogPostComment model
    comments = BlogPostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = "__all__"
        read_only_fields = ["owner"]
