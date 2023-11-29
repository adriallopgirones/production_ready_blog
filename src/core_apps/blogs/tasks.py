import requests
from celery import shared_task
from django.db import transaction

from core_apps.blogs.models import BlogPost


@shared_task
def analyze_sentiment(blog_post_uuid):
    """
    Retrieves a blog post, sends its text to an external API and updates the sentiment field.
    -----
    This is performed asynchronously by Celery (that's why we use the sared_task decorator)
    When the user creates a blog post, it gets stored right away in the database, but the
    sentiment field is left empty. This task is triggered by a signal after the blog post is created
    and updates the sentiment field.
    -----
    """
    try:
        blog_post = BlogPost.objects.get(pk=blog_post_uuid)
        querystring = {"text": blog_post.content}
        # Pretty random api from the internet for sentiment analysis
        url = f"https://nocodefunctions.com/api/sentimentForAText?text-lang=en&text={querystring}&output-format=json"

        response = requests.get(url)
        sentiment = response.json()["sentiment"]

        # If an exception occurs the entire operation is rolled back, usefule when dealing
        # with multiple database operations like here reading-update
        with transaction.atomic():
            blog_post.sentiment = sentiment
            blog_post.save()

    except BlogPost.DoesNotExist:
        # TODO: logging
        print(f"Blog Post with id {blog_post_uuid} does not exist.")
    except Exception as e:
        print(f"Error analyzing sentiment for article {blog_post_uuid}: {str(e)}")
