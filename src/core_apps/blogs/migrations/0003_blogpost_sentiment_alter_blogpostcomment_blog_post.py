# Generated by Django 4.2.7 on 2023-11-28 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogs", "0002_blogpostcomment"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="sentiment",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="blogpostcomment",
            name="blog_post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="blogs.blogpost",
            ),
        ),
    ]
