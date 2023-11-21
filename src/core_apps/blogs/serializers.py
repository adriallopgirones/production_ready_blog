from rest_framework import serializers
from blogs.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"
        read_only_fields = ["author"]
