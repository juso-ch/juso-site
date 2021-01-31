# Generated by Django 3.1 on 2020-08-21 11:54

import imagefield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0015_auto_20200821_1341"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidature",
            name="image",
            field=imagefield.fields.ImageField(
                blank=True,
                height_field="image_height",
                null=True,
                upload_to="people/",
                verbose_name="image",
                width_field="image_width",
            ),
        ),
        migrations.AddField(
            model_name="candidature",
            name="image_height",
            field=models.PositiveIntegerField(blank=True,
                                              editable=False,
                                              null=True),
        ),
        migrations.AddField(
            model_name="candidature",
            name="image_ppoi",
            field=imagefield.fields.PPOIField(default="0.5x0.5",
                                              max_length=20),
        ),
        migrations.AddField(
            model_name="candidature",
            name="image_width",
            field=models.PositiveIntegerField(blank=True,
                                              editable=False,
                                              null=True),
        ),
    ]
