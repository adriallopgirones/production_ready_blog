from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication

from core_apps.blogs.models import BlogPost
from core_apps.blogs.serializers import (
    BlogPostSerializer,
    BlogPostSerializerWithComments,
)
from core_apps.common.decorators import catch_redis_down
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

    def get_serializer_class(self):
        if self.action == "list":
            # Return serializer without comments for list action
            return BlogPostSerializer
        # Return serializer with comments for retrieve action
        return BlogPostSerializerWithComments

    def get_queryset(self):
        if self.action == "retrieve":
            # prefetch_related performs a more efficient query by fetching the related objects
            # in a single query, rather than one query per object. (SQL join)
            # Making different queries for related objects can lead to N+1 problem.

            return BlogPost.objects.all().prefetch_related("comments")
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Doing per-view caching, we'll store the result of this view in the cache for 5 minutes using redis
    @method_decorator(
        catch_redis_down(cache_page(60 * 1))
    )  # Cache the response for 5 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    """
    What we do above is useful if we are interested in caching the entire response, if we need something
    more specific like returning a feed to a user (every user needs a different response) we could use
    @method_decorator(cache_page(60 * 5, key_func=_made_up_name_unique_for_each_user))
    or use from django.core.cache import cache cache.set() and cache.get()
    """


class BlogPostCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
