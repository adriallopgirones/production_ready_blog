from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/blogs/", include("core_apps.blogs.urls")),
]
