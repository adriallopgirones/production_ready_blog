import uuid

from django.db import models


class BaseModel(models.Model):
    """
    All models inherit from this base model that holds common fields
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]
