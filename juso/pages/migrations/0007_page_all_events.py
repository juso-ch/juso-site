# Generated by Django 3.0.3 on 2020-02-16 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20200215_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='all_events',
            field=models.BooleanField(default=False, verbose_name='all events'),
        ),
    ]
