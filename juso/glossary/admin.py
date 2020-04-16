from django.utils.translation import gettext as _
from django.contrib import admin
from feincms3.plugins.richtext import RichTextInline
from juso.glossary.models import Entry

# Register your models here.


class GlossaryContentInline(RichTextInline):
    autocomplete_fields = [
        'entries'
    ]

    fields = [
        'text', 'entries', 'region', 'ordering'
    ]


@admin.register(Entry)
class GlossaryEntryAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]

    prepopulated_fields = {
        "slug": ("name",),
    }

    fieldsets = (
        (None, {
            'fields': ['name', 'content']
        }),
        (_("advanced"), {
            'fields': ['auto_pattern', 'pattern', 'slug'],
            'classes': ['collapse'],
        })
    )

