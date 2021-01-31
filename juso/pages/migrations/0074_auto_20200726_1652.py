# Generated by Django 3.0.5 on 2020-07-26 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0073_auto_20200726_1649"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="prefetches",
            field=models.TextField(
                default=
                "fonts/klima-regular-web.woff2:font\nfonts/klima-regular-italic-web.woff2:font\nfonts/klima-bold-web.woff2:font\nfonts/klima-bold-italic-web.woff2:font\n        ",
                help_text="files that should be preloaded",
                verbose_name="prefetch",
            ),
        ),
    ]
