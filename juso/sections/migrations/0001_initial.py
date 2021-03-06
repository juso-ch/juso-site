# Generated by Django 3.0.3 on 2020-02-15 19:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feincms3_sites", "0004_site_is_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="Section",
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
                ("name", models.CharField(max_length=100,
                                          verbose_name="Name")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="sections.Section",
                        verbose_name="parent",
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="section",
                        to="feincms3_sites.Site",
                        verbose_name="Webseite",
                    ),
                ),
                (
                    "users",
                    models.ManyToManyField(to=settings.AUTH_USER_MODEL,
                                           verbose_name="Benutzer"),
                ),
            ],
            options={
                "verbose_name": "section",
                "verbose_name_plural": "sections",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=200,
                                          verbose_name="Name")),
                ("slug", models.SlugField(verbose_name="Slug")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="sections.Category",
                        verbose_name="parent",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
