# Generated by Django 3.0.5 on 2020-05-10 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_auto_20200510_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventplugin',
            name='title',
            field=models.CharField(blank=True, max_length=180, verbose_name='Titel'),
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(max_length=180),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['start_date', 'slug', 'section'], name='events_even_start_d_4d180d_idx'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.UniqueConstraint(fields=('slug', 'start_date', 'section'), name='unique_slugs_for_section_and_date'),
        ),
    ]
