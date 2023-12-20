from django.urls import path

from core_apps.search.views import BlogPostDocumentView

urlpatterns = [
    path(
        "",
        BlogPostDocumentView.as_view(
            {"get": "list"}
        ),  # Maps GET method to list action in the view, and only handles GET requests
        name="article_search",
    )
]
