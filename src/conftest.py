import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from core_apps.blogs.models import BlogPost


@pytest.fixture
def user_client():
    user = User.objects.create_user(username="testuser", password="testpassword")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def blog_posts():
    # Create two blog posts
    user1 = User.objects.create_user(username="testuser1", password="testpassword")
    user2 = User.objects.create_user(username="testuser2", password="testpassword")
    post1 = BlogPost.objects.create(
        owner=user1, title="Test Post 1", content="Test Content 1"
    )
    post2 = BlogPost.objects.create(
        owner=user2, title="Test Post 2", content="Test Content 2"
    )
    return [post1, post2]
