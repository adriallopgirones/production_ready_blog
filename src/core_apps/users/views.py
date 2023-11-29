from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication

from core_apps.common.permissions import IsOwnerOrReadOnly
from core_apps.users import process_and_save_profile_picture
from core_apps.users.models import PublicProfile


class PublicProfileViewSet(viewsets.ModelViewSet):
    """
    When a user creates a profile with a picture or updates it, we trigger a celery task that
    handles it in the background
    """

    queryset = PublicProfile.objects.all()
    serializer_class = PublicProfile
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        self.trigger_celery_task(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self.trigger_celery_task(instance)

    def trigger_celery_task(self, instance):
        """
        Calls the celery task when a user sends a profile picture
        """
        if self.request.data.get("profile_picture"):
            profile_id = instance.id
            image_data = self.request.data.get("profile_picture")
            if image_data:
                process_and_save_profile_picture.delay(profile_id, image_data)
