# Generated by Django 3.0.5 on 2020-07-01 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0041_formentrycounterplugin"),
    ]

    operations = [
        migrations.AddField(
            model_name="formentrycounterplugin",
            name="template_key",
            field=models.CharField(
                choices=[("forms/bar.html", "bar"),
                         ("forms/number.html", "number")],
                default="forms/bar.html",
                max_length=40,
                verbose_name="template",
            ),
        ),
    ]
