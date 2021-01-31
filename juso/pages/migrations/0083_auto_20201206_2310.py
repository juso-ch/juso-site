# Generated by Django 3.1.4 on 2020-12-06 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0082_votingrecommendationplugin'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='page',
            index=models.Index(fields=['is_active', 'menu', 'language_code'], name='pages_page_is_acti_4365f3_idx'),
        ),
    ]
