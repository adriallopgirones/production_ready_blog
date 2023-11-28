from django.db.models.signals import post_save
from django.dispatch import receiver
from core_apps.blogs.models import BlogPost
from core_apps.blogs.tasks import analyze_sentiment


@receiver(post_save, sender=BlogPost)
def post_save_article(sender, instance, created, **kwargs):
    """
    Update sentiment field of BlogPost model after it's created
    """
    if created:
        analyze_sentiment.delay(instance.uuid)
