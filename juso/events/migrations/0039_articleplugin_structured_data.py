# Generated by Django 3.0.5 on 2020-06-01 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0038_auto_20200529_1624"),
    ]

    operations = [
        migrations.AddField(
            model_name="articleplugin",
            name="structured_data",
            field=models.BooleanField(default=False,
                                      verbose_name="include structured data"),
        ),
    ]
