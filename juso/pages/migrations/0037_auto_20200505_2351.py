# Generated by Django 3.0.5 on 2020-05-05 21:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0009_merge_20200324_2216"),
        ("events", "0019_auto_20200505_2351"),
        ("sections", "0007_auto_20200502_2048"),
        ("blog", "0018_auto_20200505_2351"),
        ("glossary", "0005_auto_20200505_2351"),
        ("forms", "0014_auto_20200505_2351"),
        ("pages", "0036_auto_20200505_2047"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="download",
            options={
                "verbose_name": "Download",
                "verbose_name_plural": "Downloads"
            },
        ),
        migrations.AlterField(
            model_name="articleplugin",
            name="articles",
            field=models.ManyToManyField(
                blank=True,
                related_name="_articleplugin_articles_+",
                related_query_name="+",
                to="blog.Article",
                verbose_name="Artikel",
            ),
        ),
        migrations.AlterField(
            model_name="articleplugin",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="sections.Category",
                verbose_name="Kategorie",
            ),
        ),
        migrations.AlterField(
            model_name="articleplugin",
            name="count",
            field=models.IntegerField(default=3, verbose_name="Anzahl"),
        ),
        migrations.AlterField(
            model_name="articleplugin",
            name="namespace",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="blog.NameSpace",
                verbose_name="Namensraum",
            ),
        ),
        migrations.AlterField(
            model_name="button",
            name="style",
            field=models.CharField(
                blank=True,
                choices=[("", "keine"), ("secondary", "sekundär")],
                default="",
                max_length=20,
                verbose_name="Styl",
            ),
        ),
        migrations.AlterField(
            model_name="download",
            name="download_text",
            field=models.CharField(max_length=200,
                                   verbose_name="Download Text"),
        ),
        migrations.AlterField(
            model_name="download",
            name="link_classes",
            field=models.CharField(blank=True,
                                   max_length=200,
                                   verbose_name="Link Klassen (css)"),
        ),
        migrations.AlterField(
            model_name="eventplugin",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                related_query_name="+",
                to="sections.Category",
                verbose_name="Kategorie",
            ),
        ),
        migrations.AlterField(
            model_name="eventplugin",
            name="count",
            field=models.IntegerField(default=3, verbose_name="Anzahl"),
        ),
        migrations.AlterField(
            model_name="eventplugin",
            name="events",
            field=models.ManyToManyField(
                blank=True,
                related_name="_eventplugin_events_+",
                related_query_name="+",
                to="events.Event",
                verbose_name="Events",
            ),
        ),
        migrations.AlterField(
            model_name="eventplugin",
            name="namespace",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                related_query_name="+",
                to="events.NameSpace",
                verbose_name="Namensraum",
            ),
        ),
        migrations.AlterField(
            model_name="formplugin",
            name="form",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                related_query_name="+",
                to="forms.Form",
                verbose_name="Formular",
            ),
        ),
        migrations.AlterField(
            model_name="glossaryrichtext",
            name="entries",
            field=models.ManyToManyField(
                related_name="pages_glossaryrichtext_related",
                related_query_name="pages_glossaryrichtexts",
                to="glossary.Entry",
                verbose_name="Einträge",
            ),
        ),
        migrations.AlterField(
            model_name="page",
            name="template_key",
            field=models.CharField(
                choices=[
                    ("default", "Standard"),
                    ("sidebar-right", "Sidebar-Right"),
                    ("sidebar-left", "Sidebar-Left"),
                    ("sidebar-both", "Sidebar-Both"),
                    ("fullwidth", "Fullwidth"),
                ],
                default="default",
                max_length=100,
                verbose_name="template",
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="columns",
            field=models.CharField(
                choices=[("two", "2"), ("three", "3"), ("four", "4"),
                         ("five", "5")],
                default="three",
                max_length=10,
                verbose_name="Spalten",
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="people.Team",
                verbose_name="Team",
            ),
        ),
    ]
