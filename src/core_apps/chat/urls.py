from django.urls import include, path
from rest_framework import routers

from core_apps.chat.views import MessageViewSet

urlpatterns = []

router = routers.DefaultRouter()
router.register(r"", MessageViewSet, basename="chat")

urlpatterns = [
    path("", include(router.urls)),
]
