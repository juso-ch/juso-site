# Generated by Django 3.0.5 on 2020-06-05 15:21

import imagefield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0055_page_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="favicon",
            field=imagefield.fields.ImageField(
                blank=True,
                height_field="favicon_height",
                upload_to="",
                verbose_name="favicon",
                width_field="favicon_width",
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="favicon_height",
            field=models.PositiveIntegerField(blank=True,
                                              editable=False,
                                              null=True),
        ),
        migrations.AddField(
            model_name="page",
            name="favicon_ppoi",
            field=imagefield.fields.PPOIField(default="0.5x0.5",
                                              max_length=20),
        ),
        migrations.AddField(
            model_name="page",
            name="favicon_width",
            field=models.PositiveIntegerField(blank=True,
                                              editable=False,
                                              null=True),
        ),
        migrations.AddField(
            model_name="page",
            name="primary_color",
            field=models.CharField(blank=True,
                                   max_length=7,
                                   verbose_name="primary color"),
        ),
    ]
