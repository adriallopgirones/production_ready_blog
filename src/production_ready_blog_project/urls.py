from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # TODO: Look into something more robust for authentication
    path("api/v1/api-token-auth/", views.obtain_auth_token),
    path("api/v1/blog_posts/", include("core_apps.blogs.urls")),
    path("api/v1/public_profiles/", include("core_apps.users.urls")),
    path("api/v1/chats/", include("core_apps.chat.urls")),
]
