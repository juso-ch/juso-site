# Reconciles model state with the DB. The template_key choices change is
# state-only (no SQL). The index already exists in production (it was created
# outside migration history), so it is added idempotently: CREATE INDEX IF NOT
# EXISTS keeps this safe on production while still creating it on fresh DBs.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0090_testimonialplugin_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='template_key',
            field=models.CharField(choices=[('default', 'Default'), ('feature_top', 'Feature_Top')], default='default', max_length=100, verbose_name='template'),
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddIndex(
                    model_name='page',
                    index=models.Index(fields=['is_active', 'menu', 'language_code'], name='pages_page_is_acti_4365f3_idx'),
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql='CREATE INDEX IF NOT EXISTS "pages_page_is_acti_4365f3_idx" ON "pages_page" ("is_active", "menu", "language_code");',
                    reverse_sql='DROP INDEX IF EXISTS "pages_page_is_acti_4365f3_idx";',
                ),
            ],
        ),
    ]
