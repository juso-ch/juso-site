# Generated by Django 3.0.5 on 2020-05-10 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0031_button_line_break"),
    ]

    operations = [
        migrations.AddField(
            model_name="button",
            name="align",
            field=models.CharField(
                blank=True,
                choices=[("", "Standard"), ("center", "center"),
                         ("right", "right")],
                max_length=30,
                verbose_name="alignment",
            ),
        ),
    ]
