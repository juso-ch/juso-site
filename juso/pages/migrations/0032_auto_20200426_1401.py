# Generated by Django 3.0.3 on 2020-04-26 14:01

import imagefield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0031_auto_20200426_1301"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="header_image",
            field=imagefield.fields.ImageField(
                blank=True,
                height_field="header_image_height",
                null=True,
                upload_to="",
                verbose_name="header image",
                width_field="header_image_width",
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="header_image_height",
            field=models.PositiveIntegerField(blank=True,
                                              editable=False,
                                              null=True),
        ),
        migrations.AddField(
            model_name="page",
            name="header_image_ppoi",
            field=imagefield.fields.PPOIField(default="0.5x0.5",
                                              max_length=20),
        ),
        migrations.AddField(
            model_name="page",
            name="header_image_width",
            field=models.PositiveIntegerField(blank=True,
                                              editable=False,
                                              null=True),
        ),
    ]
