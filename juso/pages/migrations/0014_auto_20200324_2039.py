# Generated by Django 3.0.3 on 2020-03-24 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0013_divider"),
    ]

    operations = [
        migrations.AlterField(
            model_name="button",
            name="text",
            field=models.CharField(blank=True,
                                   max_length=240,
                                   verbose_name="Text"),
        ),
        migrations.AlterField(
            model_name="divider",
            name="text",
            field=models.CharField(blank=True,
                                   max_length=240,
                                   verbose_name="Text"),
        ),
    ]
