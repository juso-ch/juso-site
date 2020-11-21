# Generated by Django 3.1 on 2020-11-21 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sections", "0014_auto_20200712_1711"),
        ("forms", "0043_auto_20200923_1926"),
    ]

    operations = [
        migrations.CreateModel(
            name="Webhook",
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
                ("name", models.CharField(max_length=200)),
                ("url", models.URLField(max_length=800)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sections.section",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WebhookField",
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
                ("form_slug", models.SlugField()),
                ("webhook_slug", models.CharField(max_length=200)),
                ("field_converter", models.CharField(max_length=200)),
                ("field_converter_args", models.CharField(max_length=200)),
                (
                    "webhook",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fields",
                        to="forms.webhook",
                    ),
                ),
            ],
        ),
    ]
