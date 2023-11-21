from django.db import models


class BaseModel(models.Model):
    """
    All models inherit from this base model that holds common fields
    """

    uuid = models.TextField(max_length=36, blank=False, null=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]
