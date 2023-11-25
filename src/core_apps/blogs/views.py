from rest_framework import viewsets, permissions
from rest_framework.authentication import (
    TokenAuthentication,
)

from core_apps.blogs.models import BlogPost
from core_apps.blogs.serializers import BlogPostSerializer
from core_apps.common.permissions import IsOwnerOrReadOnly


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
