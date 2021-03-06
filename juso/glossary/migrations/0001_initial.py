# Generated by Django 3.0.3 on 2020-04-16 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Entry",
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
                ("name", models.CharField(max_length=40, verbose_name="Name")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                (
                    "auto_pattern",
                    models.BooleanField(default=True,
                                        verbose_name="auto-pattern"),
                ),
                ("pattern",
                 models.CharField(max_length=200, verbose_name="pattern")),
                ("content", models.TextField()),
                (
                    "translations",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_entry_translations_+",
                        to="glossary.Entry",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
    ]
