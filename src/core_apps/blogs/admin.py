from django.contrib import admin
from core_apps.blogs.models import BlogPost, BlogPostComment

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(BlogPostComment)
