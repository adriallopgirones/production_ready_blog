from django.urls import include, path
from rest_framework import routers

from core_apps.blogs.views import BlogPostViewSet

# Router helps us to avoid writing url patterns like randomview/{pk}/
router = routers.DefaultRouter()
router.register(r"", BlogPostViewSet, basename="blog_post")

urlpatterns = [
    path("", include(router.urls)),
]
