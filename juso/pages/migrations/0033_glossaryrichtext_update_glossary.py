# Generated by Django 3.0.3 on 2020-04-26 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0032_auto_20200426_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='glossaryrichtext',
            name='update_glossary',
            field=models.BooleanField(default=True),
        ),
    ]
