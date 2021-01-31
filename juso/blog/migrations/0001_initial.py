# Generated by Django 3.0.3 on 2020-02-15 19:01

import django.db.models.deletion
import django.utils.timezone
import feincms3.cleanse
import imagefield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "meta_title",
                    models.CharField(
                        blank=True,
                        help_text="Used for Open Graph and other meta tags.",
                        max_length=200,
                        verbose_name="title",
                    ),
                ),
                (
                    "meta_description",
                    models.TextField(
                        blank=True,
                        help_text="Override the description for this page.",
                        verbose_name="description",
                    ),
                ),
                (
                    "meta_image",
                    imagefield.fields.ImageField(
                        blank=True,
                        height_field="meta_image_height",
                        help_text="Set the Open Graph image.",
                        upload_to="meta/%Y/%m",
                        verbose_name="image",
                        width_field="meta_image_width",
                    ),
                ),
                (
                    "meta_canonical",
                    models.URLField(
                        blank=True,
                        help_text="If you need this you probably know.",
                        verbose_name="canonical URL",
                    ),
                ),
                (
                    "meta_author",
                    models.CharField(
                        blank=True,
                        help_text="Override the author meta tag.",
                        max_length=200,
                        verbose_name="author",
                    ),
                ),
                (
                    "meta_robots",
                    models.CharField(
                        blank=True,
                        help_text="Override the robots meta tag.",
                        max_length=200,
                        verbose_name="robots",
                    ),
                ),
                (
                    "meta_image_width",
                    models.PositiveIntegerField(blank=True,
                                                editable=False,
                                                null=True),
                ),
                (
                    "meta_image_height",
                    models.PositiveIntegerField(blank=True,
                                                editable=False,
                                                null=True),
                ),
                (
                    "meta_image_ppoi",
                    imagefield.fields.PPOIField(default="0.5x0.5",
                                                max_length=20),
                ),
                (
                    "template_key",
                    models.CharField(
                        choices=[
                            ("default", "Default"),
                            ("sidebar-right", "Sidebar-Right"),
                            ("sidebar-left", "Sidebar-Left"),
                            ("fullwidth", "Fullwidth"),
                        ],
                        default="default",
                        max_length=100,
                        verbose_name="template",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        choices=[("de", "German"), ("fr", "French"),
                                 ("it", "Italian")],
                        default="de",
                        max_length=10,
                        verbose_name="language",
                    ),
                ),
                ("title", models.CharField(max_length=200,
                                           verbose_name="Titel")),
                ("slug", models.SlugField(verbose_name="Slug")),
                (
                    "publication_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="publication date",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(auto_now_add=True,
                                         verbose_name="created at"),
                ),
                (
                    "edited_date",
                    models.DateTimeField(auto_now=True,
                                         verbose_name="edited at"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Autor",
                    ),
                ),
            ],
            options={
                "verbose_name": "article",
                "verbose_name_plural": "articles",
            },
        ),
        migrations.CreateModel(
            name="NameSpace",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        choices=[("de", "German"), ("fr", "French"),
                                 ("it", "Italian")],
                        default="de",
                        max_length=10,
                        verbose_name="language",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField()),
            ],
            options={
                "verbose_name": "name space",
                "verbose_name_plural": "name spaces",
                "ordering": ["slug"],
            },
        ),
        migrations.CreateModel(
            name="RichText",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text",
                 feincms3.cleanse.CleansedRichTextField(verbose_name="text")),
                ("region", models.CharField(max_length=255)),
                ("ordering", models.IntegerField(default=0)),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog_richtext_set",
                        to="blog.Article",
                    ),
                ),
            ],
            options={
                "verbose_name": "rich text",
                "verbose_name_plural": "rich texts",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    imagefield.fields.ImageField(
                        height_field="height",
                        upload_to="images/%Y/%m",
                        verbose_name="image",
                        width_field="width",
                    ),
                ),
                (
                    "width",
                    models.PositiveIntegerField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="image width",
                    ),
                ),
                (
                    "height",
                    models.PositiveIntegerField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="image height",
                    ),
                ),
                (
                    "ppoi",
                    imagefield.fields.PPOIField(
                        default="0.5x0.5",
                        max_length=20,
                        verbose_name="primary point of interest",
                    ),
                ),
                ("region", models.CharField(max_length=255)),
                ("ordering", models.IntegerField(default=0)),
                (
                    "caption",
                    models.CharField(blank=True,
                                     max_length=200,
                                     verbose_name="caption"),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog_image_set",
                        to="blog.Article",
                    ),
                ),
            ],
            options={
                "verbose_name": "image",
                "verbose_name_plural": "images",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="HTML",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "html",
                    models.TextField(
                        help_text=
                        "The content will be inserted directly into the page. It is VERY important that the HTML snippet is well-formed!",
                        verbose_name="HTML",
                    ),
                ),
                ("region", models.CharField(max_length=255)),
                ("ordering", models.IntegerField(default=0)),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog_html_set",
                        to="blog.Article",
                    ),
                ),
            ],
            options={
                "verbose_name": "HTML",
                "verbose_name_plural": "HTML",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="External",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField(verbose_name="URL")),
                ("region", models.CharField(max_length=255)),
                ("ordering", models.IntegerField(default=0)),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog_external_set",
                        to="blog.Article",
                    ),
                ),
            ],
            options={
                "verbose_name": "external content",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Download",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "document",
                    models.FileField(upload_to="downloads/",
                                     verbose_name="Datei"),
                ),
                (
                    "download_text",
                    models.CharField(max_length=200,
                                     verbose_name="download text"),
                ),
                (
                    "link_classes",
                    models.CharField(blank=True,
                                     max_length=200,
                                     verbose_name="link classes (css)"),
                ),
                ("region", models.CharField(max_length=255)),
                ("ordering", models.IntegerField(default=0)),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog_download_set",
                        to="blog.Article",
                    ),
                ),
            ],
            options={
                "verbose_name": "download",
                "verbose_name_plural": "downloads",
                "abstract": False,
            },
        ),
    ]
