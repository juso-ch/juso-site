# Generated by Django 3.0.3 on 2020-04-16 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("glossary", "0002_auto_20200416_2104"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entry",
            name="pattern",
            field=models.CharField(blank=True,
                                   max_length=200,
                                   verbose_name="pattern"),
        ),
    ]
