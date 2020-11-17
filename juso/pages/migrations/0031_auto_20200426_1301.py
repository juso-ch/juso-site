# Generated by Django 3.0.3 on 2020-04-26 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0030_auto_20200416_2203"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="formplugin",
            options={},
        ),
        migrations.AlterField(
            model_name="page",
            name="menu",
            field=models.CharField(
                blank=True,
                choices=[
                    ("main", "main navigation"),
                    ("top", "top navigation"),
                    ("buttons", "button navigation"),
                    ("footer", "footer navigation"),
                    ("quicklink", "quickinks"),
                ],
                default="main",
                max_length=20,
                verbose_name="menu",
            ),
        ),
    ]
