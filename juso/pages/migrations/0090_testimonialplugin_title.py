# Generated by Django 3.2.4 on 2021-06-24 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0089_auto_20210624_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonialplugin',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
