# Generated by Django 3.0.5 on 2020-05-07 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0019_auto_20200505_2351"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="articleplugin",
            options={
                "verbose_name": "article plugin",
                "verbose_name_plural": "article plugins",
            },
        ),
        migrations.AlterModelOptions(
            name="eventplugin",
            options={
                "verbose_name": "event plugin",
                "verbose_name_plural": "event plugins",
            },
        ),
        migrations.AlterModelOptions(
            name="namespace",
            options={
                "ordering": ["name"],
                "verbose_name": "Namensraum",
                "verbose_name_plural": "namespaces",
            },
        ),
    ]
