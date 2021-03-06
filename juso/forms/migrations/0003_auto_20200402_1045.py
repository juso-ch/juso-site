# Generated by Django 3.0.3 on 2020-04-02 10:45

import django.db.models.deletion
import feincms3.cleanse
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0002_auto_20200331_2009"),
    ]

    operations = [
        migrations.AddField(
            model_name="form",
            name="submit",
            field=models.CharField(default="Submit", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="form",
            name="success_message",
            field=models.TextField(blank=True, verbose_name="success message"),
        ),
        migrations.AddField(
            model_name="form",
            name="success_redirect",
            field=models.URLField(blank=True, verbose_name="success redirect"),
        ),
        migrations.AlterField(
            model_name="formfield",
            name="help_text",
            field=models.CharField(blank=True,
                                   max_length=240,
                                   verbose_name="help text"),
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
                        related_name="forms_richtext_set",
                        to="forms.Form",
                    ),
                ),
            ],
            options={
                "verbose_name": "rich text",
            },
        ),
    ]
