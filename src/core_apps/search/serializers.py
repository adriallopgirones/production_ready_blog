from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from core_apps.search.documents import BlogPostDocument


class BlogPostESSerializer(DocumentSerializer):
    class Meta:
        document = BlogPostDocument
        fields = ["title", "author", "created_at", "sentiment", "content"]
