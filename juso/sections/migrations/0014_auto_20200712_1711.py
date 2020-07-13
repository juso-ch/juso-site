# Generated by Django 3.0.5 on 2020-07-12 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sections", "0013_auto_20200626_1201"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="category",
            index=models.Index(fields=["slug"], name="sections_ca_slug_94ece0_idx"),
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(
                fields=("slug", "language_code"), name="unique_slug_for_language"
            ),
        ),
    ]
