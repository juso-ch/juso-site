from content_editor.admin import ContentEditor
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from feincms3 import plugins
from feincms3_meta.models import MetaMixin
from js_asset import JS

from juso.admin import ButtonInline
from juso.blog import plugins as blog_plugins
from juso.blog import models
from juso.blog.models import Article, NameSpace
from juso.events import plugins as event_plugins
from juso.forms import plugins as form_plugins
from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.utils import CopyContentMixin
from juso.glossary.admin import GlossaryContentInline

# Register your models here.


@admin.register(Article)
class ArticleAdmin(ContentEditor, CopyContentMixin):

    list_display = [
        'title',
        'slug',
        'publication_date',
        'category',
        'section',
        'language_code',
        'namespace',
    ]

    list_filter = [
        'category',
        'author',
        'section',
        'namespace',
        'language_code',
    ]

    list_editable = [
        'language_code',
        'slug',
    ]

    date_hierarchy = 'publication_date'

    autocomplete_fields = [
        'category',
        'namespace',
        'author',
        'section',
        'translations',
    ]

    search_fields = [
        'title',
        'blog_richtext_set__text',
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
                'author',
                'category',
                'tags',
            )
        }),
        (_('settings'), {
            'classes': ('tabbed',),
            'fields': (
                'language_code',
                'slug',
                ('publication_date', 'created_date', 'edited_date'),
                'section',
                'namespace',
                'template_key',
                'header_image',
                'header_image_ppoi'
            )
        }),
        MetaMixin.admin_fieldset(),
        (_("translations"), {
            'classes': ('tabbed', ),
            'fields': (
                'translations',
            )
        })
    )

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External),
        ButtonInline.create(models.Button),
        download.DownloadInline.create(models.Download),
        people_plugins.TeamPluginInline.create(models.Team),
        GlossaryContentInline.create(models.GlossaryRichText),
        blog_plugins.ArticlePluginInline.create(models.ArticlePlugin),
        event_plugins.EventPluginInline.create(models.EventPlugin),
        form_plugins.FormPluginInline.create(models.FormPlugin),
    ]

    plugins = models.plugins
    actions = ['copy_selected']

    class Media:
        js = (
            'admin/js/jquery.init.js',
            JS('https://kit.fontawesome.com/91a6274901.js', {
                'async': 'async',
                'crossorigin': 'anonymous',
            }, static=False),
            'admin/plugin_buttons.js',
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        section_field = form.base_fields['section']

        sections = request.user.section_set.all()
        section_field.initial = sections[0]

        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(section__in=sections)


@admin.register(NameSpace)
class NamespaceAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]

    list_display = [
        'name',
        'slug',
        'language_code',
    ]

    list_filter = [
        'language_code'
    ]

    prepopulated_fields = {
        "slug": ("name",)
    }

    autocomplete_fields = ('translations',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'language_code', 'translations')
        }),
    )

class WPImportMappingInline(admin.TabularInline):
    model = models.NamespaceMapping
    extra = 3

    autocomplete_fields = ['target']

@admin.register(models.WPImport)
class WPImportAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'section', 'default_namespace'
    ]

    inlines = [
        WPImportMappingInline
    ]
