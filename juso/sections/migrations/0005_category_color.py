# Generated by Django 3.0.3 on 2020-04-26 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sections", "0004_auto_20200329_1551"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="color",
            field=models.CharField(default="#ff000",
                                   max_length=7,
                                   verbose_name="color"),
        ),
    ]
