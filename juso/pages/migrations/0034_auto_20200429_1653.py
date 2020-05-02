# Generated by Django 3.0.3 on 2020-04-29 16:53

from django.db import migrations, models
import django.db.models.deletion
import juso.models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0012_auto_20200426_1301'),
        ('pages', '0033_glossaryrichtext_update_glossary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='header',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='button',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='button',
            name='inverted',
        ),
        migrations.AlterField(
            model_name='button',
            name='color',
            field=juso.models.ColorField(blank=True, choices=[('red', 'red'), ('orange', 'orange'), ('yellow', 'yellow'), ('olive', 'olive'), ('green', 'green'), ('teal', 'teal'), ('violett', 'violett'), ('purple', 'purple'), ('pink', 'pink'), ('brown', 'brown'), ('grey', 'grey'), ('black', 'black')], max_length=20),
        ),
        migrations.AlterField(
            model_name='button',
            name='style',
            field=models.CharField(blank=True, choices=[('', 'none'), ('secondary', 'secondary')], default='', max_length=20, verbose_name='style'),
        ),
        migrations.AlterField(
            model_name='formplugin',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='+', to='forms.Form', verbose_name='form'),
        ),
        migrations.DeleteModel(
            name='Divider',
        ),
        migrations.DeleteModel(
            name='Header',
        ),
    ]
