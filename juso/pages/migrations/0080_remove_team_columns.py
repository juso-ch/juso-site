# Generated by Django 3.1 on 2020-08-21 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0079_candidatureplugin"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="columns",
        ),
    ]
