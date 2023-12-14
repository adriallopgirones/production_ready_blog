from django.contrib.auth.models import User
from django.db import models

from core_apps.common.models import BaseModel


class Message(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    room_group_name = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self) -> str:
        return f"{self.owner.username} on {self.room_group_name}: {self.message}"
