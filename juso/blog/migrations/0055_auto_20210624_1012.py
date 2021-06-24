# Generated by Django 3.2.4 on 2021-06-24 08:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0054_auto_20210624_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='meta_card_type',
            field=models.CharField(blank=True, choices=[('summary', 'summary'), ('summary_large_image', 'summary large image'), ('player', 'player')], help_text='Card type', max_length=50, verbose_name='twitter card type'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_player',
            field=models.CharField(blank=True, help_text='HTTPS URL to iFrame player.', max_length=600, verbose_name='player url'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_player_height',
            field=models.IntegerField(default=1080, verbose_name='player height'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_player_width',
            field=models.IntegerField(default=1920, verbose_name='player width'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_twitter_site',
            field=models.CharField(blank=True, help_text='The Twitter @username the card should be attributed to.', max_length=30, verbose_name='twitter site'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_video',
            field=models.FileField(blank=True, help_text='Set the Open Graph video.', upload_to='meta/video/%Y/%m', validators=[django.core.validators.FileExtensionValidator(['mp4'])], verbose_name='video'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_video_height',
            field=models.IntegerField(default=1080, verbose_name='video height'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_video_url',
            field=models.URLField(blank=True, help_text='Set the Open Graph video to an url.', verbose_name='video url'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_video_width',
            field=models.IntegerField(default=1920, verbose_name='video width'),
        ),
    ]
