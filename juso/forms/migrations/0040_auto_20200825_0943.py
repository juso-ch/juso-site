# Generated by Django 3.1 on 2020-08-25 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0039_auto_20200825_0931"),
    ]

    operations = [
        migrations.RenameField(
            model_name="mailchimpconnection",
            old_name="mailchimp_api_key",
            new_name="api_key",
        ),
        migrations.RenameField(
            model_name="mailchimpconnection",
            old_name="mailchimp_api_server",
            new_name="api_server",
        ),
    ]
