from content_editor.admin import ContentEditor
from django.contrib import admin
from django.utils.translation import gettext as _
from feincms3 import plugins
from feincms3.admin import TreeAdmin
from feincms3_sites.admin import SiteAdmin
from feincms3_sites.models import Site
from js_asset import JS

from fomantic_ui import models as fomantic
from juso.pages import models
from juso.people import plugins as people_plugins
from juso.events import plugins as event_plugins
from juso.blog import plugins as blog_plugins
from juso.forms import plugins as form_plugins
from juso.plugins import download
from juso.utils import CopyContentMixin

# Register your models here.


class PageAdmin(CopyContentMixin, ContentEditor, TreeAdmin):
    list_display = [
        "indented_title",
        "move_column",
        'slug',
        'static_path',
        'path',
        "is_active",
        'language_code',
        "template_key",
        'application',
    ]
    actions = ['copy_selected']

    prepopulated_fields = {'slug': ('title',)}

    autocomplete_fields = [
        'site',
        'parent',
        'blog_namespace',
        'category',
        'redirect_to_page',
        'translations',
        'featured_categories',
        'sections',
    ]

    search_fields = ['title']
    list_editable = [
        'is_active',
        'slug',
        'static_path',
        'path',
        'language_code',
    ]

    list_filter = ['is_active', 'menu', 'language_code', 'site']

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External),
        download.DownloadInline.create(models.Download),
        fomantic.ButtonInline.create(models.Button),
        fomantic.DividerInline.create(models.Divider),
        fomantic.HeaderInline.create(models.Header),
        people_plugins.TeamPluginInline.create(models.Team),
        event_plugins.EventPluginInline.create(models.EventPlugin),
        blog_plugins.ArticlePluginInline.create(models.ArticlePlugin),
        form_plugins.FormPluginInline.create(models.FormPlugin),
    ]

    plugins = models.plugins

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'parent',
            )
        }),
        (_('settings'), {
            'classes': ('tabbed',),
            'fields': (
                'is_active',
                'menu',
                'language_code',
                'template_key',
                'is_landing_page',
            ),
        }),
        (_('path'), {
            'classes': ('tabbed',),
            'fields': (
                'slug',
                'static_path',
                'path',
                'site',
            )
        }),
        (_('application'), {
            'classes': ('tabbed', ),
            'fields': (
                'application',
                'category',
                'blog_namespace',
                'featured_categories',
                'sections',
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
        (_('redirect'), {
            'classes': ('tabbed',),
            'fields': (
                'redirect_to_page',
                'redirect_to_url',
            )
        }),
        (_('translations'), {
            'classes': ('tabbed',),
            'fields': ('translations',)
        }),
    )

    mptt_level_indent = 30

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

        site_field = form.base_fields['site']
        site_field.required = True

        sections = request.user.section_set.all()
        site_field.initial = Site.objects.filter(section__in=sections)[0]

        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(site__section__in=sections)


class SiteAdmin(SiteAdmin):
    search_fields = ['domain']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(section__in=sections)


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
admin.site.register(models.Page, PageAdmin)
