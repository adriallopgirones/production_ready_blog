from rest_framework import viewsets, permissions
from rest_framework.authentication import (
    TokenAuthentication,
)

from core_apps.users.models import PublicProfile
from core_apps.blogs.models import BlogPost
from core_apps.blogs.serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        # Retrieve the Public Profile of the user
        user_profile = PublicProfile.objects.get(user=self.request.user)
        serializer.save(author=user_profile)
