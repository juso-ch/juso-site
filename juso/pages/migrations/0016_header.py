# Generated by Django 3.0.3 on 2020-03-24 20:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0015_remove_divider_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=240, verbose_name='Text')),
                ('inverted', models.BooleanField(default=False, verbose_name='inverted')),
                ('color', models.CharField(blank=True, choices=[('red', 'red')], max_length=20)),
                ('level', models.SmallIntegerField(choices=[(1, 'h1'), (2, 'h2'), (3, 'h3'), (4, 'h4'), (5, 'h5')], verbose_name='level')),
                ('block', models.BooleanField(verbose_name='block')),
                ('dividing', models.BooleanField(verbose_name='dividing')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages_header_set', to='pages.Page')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
