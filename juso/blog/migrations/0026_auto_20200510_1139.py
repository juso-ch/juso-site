# Generated by Django 3.0.5 on 2020-05-10 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0009_auto_20200507_1758'),
        ('blog', '0025_auto_20200509_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleplugin',
            name='sections',
            field=models.ManyToManyField(blank=True, related_name='blog_articleplugin', to='sections.Section'),
        ),
    ]
