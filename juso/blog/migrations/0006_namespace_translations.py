# Generated by Django 3.0.3 on 2020-03-02 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_article_translations'),
    ]

    operations = [
        migrations.AddField(
            model_name='namespace',
            name='translations',
            field=models.ManyToManyField(related_name='_namespace_translations_+', to='blog.NameSpace'),
        ),
    ]