from django.urls import include, path
from rest_framework import routers

from core_apps.users.views import PublicProfileViewSet

# Router helps us to avoid writing url patterns like randomview/{pk}/
router = routers.DefaultRouter()
router.register(r"", PublicProfileViewSet, basename="public_profile")

urlpatterns = [
    path("", include(router.urls)),
]
