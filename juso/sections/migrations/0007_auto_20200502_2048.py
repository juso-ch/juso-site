# Generated by Django 3.0.5 on 2020-05-02 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sections", "0006_auto_20200429_1939"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="color",
            field=models.CharField(blank=True,
                                   max_length=7,
                                   verbose_name="color"),
        ),
    ]
