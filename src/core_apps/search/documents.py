from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from core_apps.blogs.models import BlogPost


@registry.register_document
class BlogPostDocument(Document):
    title = fields.TextField(
        attr="title",
        fields={
            # To be able to use autocompletion in the client for the title
            "suggest": fields.CompletionField(),
        },
    )
    sentiment = fields.TextField(
        attr="sentiment",
    )
    author_name = fields.TextField(
        fields={
            "suggest": fields.CompletionField(),
        },
    )
    content = fields.TextField(
        attr="content",
    )

    def prepare_author_name(self, instance):
        """
        When creating the indeces, ES will call this method automatically, because
        it is prefixed like 'prepare_<field_name>'
        """
        return instance.owner.public_profile.name

    class Index:
        name = "blog_posts"
        # Sharding enables horizontal scaling, and replicas are used for fault tolerance
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = BlogPost
        # Fields from BlogPost coming from a parent model
        fields = ["created_at"]
