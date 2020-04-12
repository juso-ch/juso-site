from django.contrib import admin

from content_editor.admin import ContentEditor, ContentEditorInline
from django.utils.translation import gettext as _
# Register your models here.
from feincms3 import plugins

from juso.forms.models import Form, FormField, RichText
from juso.utils import CopyContentMixin


class FormFieldInline(ContentEditorInline):
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'slug', 'input_type', 'required'),
                'ordering',
                'region'
            )
        }),
        (_("advanced"), {
            'classes': ('collapse',),
            'fields': (
                'chesoices',
                'initial',
                'help_text',
            )
        })
    )


@admin.register(Form)
class FormAdmin(ContentEditor, CopyContentMixin):
    list_display = [
        'title',
        'slug',
        'created_date',
        'section',
        'language_code',
    ]

    list_filter = [
        'section',
        'language_code',
    ]

    autocomplete_fields = [
        'section'
    ]

    search_fields = [
        'title',
    ]

    prepopulated_fields = {
        "slug": ("title",),
    }

    readonly_fields = (
        'created_date',
        'edited_date',
    )

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'section',
                'created_date',
                'edited_date',
            )
        }),
        (_("settings"), {
            'classes': ('tabbed', ),
            'fields': (
                'submit',
                'success_message',
                'success_redirect',
            )
        }),
        (_('meta'), {
            'classes': ('tabbed', ),
            'fields': (
                'meta_title',
                'meta_author',
                'meta_description',
                'meta_image',
                'meta_image_ppoi',
                'meta_robots',
                'meta_canonical',
            )
        }),
        (_("translations"), {
            'classes': ('tabbed', ),
            'fields': (
                'translations',
            )
        })
    )

    inlines = [
        FormFieldInline.create(FormField),
        plugins.richtext.RichTextInline.create(RichText),
    ]

    plugins = [FormField, RichText]
