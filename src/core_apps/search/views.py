from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from core_apps.search.documents import BlogPostDocument
from core_apps.search.serializers import BlogPostESSerializer


class BlogPostDocumentView(DocumentViewSet):
    """
    Endpoint for Blog Posts powered by Elasticsearch, allows text search and auto suggestion
    """

    document = BlogPostDocument
    serializer_class = BlogPostESSerializer

    filter_backends = [
        FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = ("title", "content", "sentiment")

    # We could filter by fields if we wanted to
    filter_fields = {}

    suggester_fields = {
        "title": {
            "field": "title.suggest",
            "suggesters": [
                SUGGESTER_COMPLETION,
            ],
        },
        "content": {
            "field": "content.suggest",
            "suggesters": [
                SUGGESTER_COMPLETION,
            ],
        },
    }
