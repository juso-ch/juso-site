# Generated by Django 3.1 on 2020-08-21 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0015_auto_20200821_1341'),
        ('events', '0050_auto_20200726_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidaturePlugin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('candidate_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='people.candidatelist', verbose_name='candidate_list')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_candidatureplugin_set', to='events.event')),
            ],
            options={
                'verbose_name': 'candidate list',
                'verbose_name_plural': 'candidate lists',
                'abstract': False,
            },
        ),
    ]
