from django.urls import path, include
from core_apps.blogs.views import BlogPostViewSet
from rest_framework import routers

# Router helps us to avoid writing url patterns like randomview/{pk}/
router = routers.DefaultRouter()
router.register(r"", BlogPostViewSet, basename="blog_post")

print(router.urls)
urlpatterns = [
    path("", include(router.urls)),
]
