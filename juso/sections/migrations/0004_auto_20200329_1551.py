# Generated by Django 3.0.3 on 2020-03-29 15:51

import imagefield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0003_auto_20200302_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='meta_author',
            field=models.CharField(blank=True, help_text='Override the author meta tag.', max_length=200, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_canonical',
            field=models.URLField(blank=True, help_text='If you need this you probably know.', verbose_name='canonical URL'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=models.TextField(blank=True, help_text='Override the description for this page.', verbose_name='description'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_image',
            field=imagefield.fields.ImageField(blank=True, height_field='meta_image_height', help_text='Set the Open Graph image.', upload_to='meta/%Y/%m', verbose_name='image', width_field='meta_image_width'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_image_height',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_image_ppoi',
            field=imagefield.fields.PPOIField(default='0.5x0.5', max_length=20),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_image_width',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_robots',
            field=models.CharField(blank=True, help_text='Override the robots meta tag.', max_length=200, verbose_name='robots'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Used for Open Graph and other meta tags.', max_length=200, verbose_name='title'),
        ),
    ]