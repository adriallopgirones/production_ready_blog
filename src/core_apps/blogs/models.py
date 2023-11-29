from django.contrib.auth.models import User
from django.db import models

from core_apps.common.models import BaseModel


class BlogPost(BaseModel):
    """
    Blog Post from a user
    """

    title = models.TextField(max_length=150, blank=False, null=False)
    content = models.TextField(max_length=500, blank=False, null=False)
    sentiment = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.owner}"


class BlogPostComment(BaseModel):
    """
    Comment to a Blog Post from a user
    """

    body = models.TextField(max_length=150, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return f" Comment to {self.blog_post} by {self.owner}"
