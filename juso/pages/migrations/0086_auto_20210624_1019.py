# Generated by Django 3.2.4 on 2021-06-24 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0003_auto_20210624_1012'),
        ('pages', '0085_auto_20210624_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='testimonials.campaign', verbose_name='campaign'),
        ),
        migrations.AlterField(
            model_name='page',
            name='application',
            field=models.CharField(blank=True, choices=[('blog', 'blog'), ('people', 'people'), ('events', 'events'), ('categories', 'categories'), ('glossary', 'glossary'), ('collection', 'collection'), ('testimonial', 'testimonial')], max_length=20, verbose_name='application'),
        ),
    ]
