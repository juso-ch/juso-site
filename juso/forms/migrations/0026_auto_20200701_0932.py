# Generated by Django 3.0.5 on 2020-07-01 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0025_delete_richtext"),
    ]

    operations = [
        migrations.AlterField(
            model_name="formfield",
            name="input_type",
            field=models.CharField(
                choices=[
                    ("text", "text"),
                    ("long_text", "long text"),
                    ("email", "email"),
                    ("boolean", "boolean"),
                    ("date", "date"),
                    ("datetime", "datetime"),
                    ("time", "time"),
                    ("decimal", "decimal"),
                    ("file", "file"),
                    ("image", "image"),
                    ("int", "integer"),
                    ("choice", "choice"),
                    ("multi", "multiple choice"),
                    ("url", "url"),
                    ("hidden", "hidden"),
                    ("section", "section"),
                ],
                max_length=140,
                verbose_name="type",
            ),
        ),
    ]
