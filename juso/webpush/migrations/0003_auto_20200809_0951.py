# Generated by Django 3.1 on 2020-08-09 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webpush", "0002_subscription_failed_attempts"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="subscription_info",
            field=models.JSONField(),
        ),
    ]