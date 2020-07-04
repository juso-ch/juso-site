from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from feincms3.plugins.richtext import RichTextInline
from reversion.admin import VersionAdmin

from juso.glossary.models import Entry

# Register your models here.


class GlossaryContentInline(RichTextInline):
    autocomplete_fields = ["entries"]

    fieldsets = (
        (None, {"fields": ["text", "entries", "region", "ordering",]}),
        (
            _("advanced"),
            {"fields": ["update_glossary", "glossary_text"], "classes": ["collapse"]},
        ),
    )


@admin.register(Entry)
class GlossaryEntryAdmin(VersionAdmin, admin.ModelAdmin):
    search_fields = ["name"]

    prepopulated_fields = {
        "slug": ("name",),
    }

    list_filter = ["category", "language_code"]

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "name",
                    "content",
                    "category",
                    "language_code",
                    "translations",
                ]
            },
        ),
        (
            _("advanced"),
            {"fields": ["auto_pattern", "pattern", "slug"], "classes": ["collapse"],},
        ),
    )

    autocomplete_fields = ["category", "translations"]
