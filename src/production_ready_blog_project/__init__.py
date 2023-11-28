from __future__ import absolute_import

# Make sure celery is always imported and instantiated when Django starts
from .celery import app as celery_app

# If you do from production_ready_blog_project import * you'll only import celery_app
__all__ = ("celery_app",)
