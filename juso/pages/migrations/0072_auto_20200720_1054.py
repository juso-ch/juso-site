# Generated by Django 3.0.5 on 2020-07-20 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0071_auto_20200714_2037'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='page',
            constraint=models.UniqueConstraint(fields=('path', 'site_id'), name='unique_page_for_path'),
        ),
    ]