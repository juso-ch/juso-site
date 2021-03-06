# Generated by Django 3.0.5 on 2020-07-21 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0048_article_author"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="article",
            constraint=models.UniqueConstraint(fields=("slug", "namespace_id",
                                                       "section_id"),
                                               name="unique_path"),
        ),
    ]
