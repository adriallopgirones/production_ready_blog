from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication

from core_apps.common.permissions import IsOwnerOrReadOnly
from core_apps.users.models import PublicProfile
from core_apps.users.serializers import PublicProfileSerializer


class PublicProfileViewSet(viewsets.ModelViewSet):
    queryset = PublicProfile.objects.all()
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
