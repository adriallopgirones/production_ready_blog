from django.urls import include, path
from rest_framework import routers

from core_apps.search.views import BlogPostDocumentView

router = routers.DefaultRouter()
router.register(r"", BlogPostDocumentView, basename="blog_post_document")
urlpatterns = [
    path("", include(router.urls)),
]
