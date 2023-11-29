from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication

from core_apps.blogs.models import BlogPost
from core_apps.blogs.serializers import BlogPostSerializer
from core_apps.common.permissions import IsOwnerOrReadOnly


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    Endpoint for getting and creating blog posts, when a user hits the list url we return
    only posts (don't want to create over-fetching), when a user hits the detail url we return
    the post with the comments, we achieve this by overriding get_queyset which seems an elegant way to do it
    """

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if self.action == "retrieve":
            # prefetch_related performs a more efficient query by fetching the related objects
            # in a single query, rather than one query per object. (SQL join)
            # Making different queries for related objects can lead to N+1 problem.

            return BlogPost.objects.all().prefetch_related("comments")
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BlogPostCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
