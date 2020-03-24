# Generated by Django 3.0.3 on 2020-03-02 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0007_team_translations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='translations',
            field=models.ManyToManyField(blank=True, related_name='_team_translations_+', to='people.Team'),
        ),
    ]
