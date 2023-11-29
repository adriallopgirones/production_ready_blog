# TODO: Does the default User model from Django works well enough for us?
from django.contrib.auth.models import User
from django.db import models

from core_apps.common.models import BaseModel


class PublicProfile(BaseModel):
    """
    Wraps a user in a PublicProfile that contain information that can be shared among other users
    """

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=150, blank=True, null=False)
    description = models.TextField(max_length=500, blank=True, null=False)
    # It stores it under MEDIA_ROOT/profile_pictures
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", default="/profile_default.png", blank=True
    )

    def __str__(self):
        return f"{self.name} with owner id {self.owner}"
