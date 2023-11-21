from django.urls import path, include
from core_apps.blogs.views import BlogPostViewSet
from rest_framework import routers

# Router helps us to avoid writing url patterns like randomview/{pk}/
router = routers.DefaultRouter()
router.register(r"blog_posts", BlogPostViewSet, basename="blog_post")

urlpatterns = [
    path("", include(router.urls)),
]
