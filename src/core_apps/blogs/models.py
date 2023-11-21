from django.db import models
from core_apps.users.models import PublicProfile


class BlogPost(models.Model):
    """
    Model for a blog post
    """

    title = models.TextField(max_length=150, blank=False, null=False)
    content = models.TextField(max_length=500, blank=False, null=False)
    author = models.ForeignKey(PublicProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.author}"
