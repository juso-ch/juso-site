# Generated by Django 3.1 on 2020-08-21 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0015_auto_20200821_1341"),
        ("pages", "0078_auto_20200813_1342"),
    ]

    operations = [
        migrations.CreateModel(
            name="CandidaturePlugin",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("region", models.CharField(max_length=255)),
                ("ordering", models.IntegerField(default=0)),
                (
                    "candidate_list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="people.candidatelist",
                        verbose_name="candidate_list",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pages_candidatureplugin_set",
                        to="pages.page",
                    ),
                ),
            ],
            options={
                "verbose_name": "candidate list",
                "verbose_name_plural": "candidate lists",
                "abstract": False,
            },
        ),
    ]
