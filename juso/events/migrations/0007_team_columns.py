# Generated by Django 3.0.3 on 2020-03-24 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_auto_20200324_1547"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="columns",
            field=models.IntegerField(default=3, verbose_name="columns"),
        ),
    ]
