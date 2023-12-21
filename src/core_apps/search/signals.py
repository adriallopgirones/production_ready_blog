from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

from core_apps.blogs.models import BlogPost


@receiver(post_save, sender=BlogPost)
def update_document(sender, instance=None, created=False, **kwargs):
    """
    Update the BlogPost in Elasticsearch index when an article instance is updated or created
    """
    registry.update(instance)


@receiver(post_delete, sender=BlogPost)
def delete_document(sender, instance=None, **kwargs):
    """
    Delete the BlogPost in Elasticsearch index when an article instance is deleted
    """
    registry.delete(instance)
