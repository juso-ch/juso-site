from content_editor.admin import ContentEditor
from django.contrib import admin
from django.utils.translation import gettext as _
from feincms3 import plugins
from js_asset import JS

from juso.utils import CopyContentMixin
from juso.blog import models
from juso.blog.models import Article, NameSpace

# Register your models here.


@admin.register(Article)
class ArticleAdmin(ContentEditor, CopyContentMixin):

    list_display = [
        'title',
        'slug',
        'author',
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
    ]

    search_fields = [
        'title',
        'description'
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
        })
    )

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External)
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(section__in=sections)

    def copy_selected(self, request, queryset):
        for article in queryset.all():
            old_pk = article.pk
            article.pk = None
            article.id = None
            article.slug = article.slug + '-copy'

            article.save()

            old_article = models.Article.objects.get(pk=old_pk)

            def copy_plugins(model_class):
                for plugin in model_class.objects.filter(parent=old_article):
                    plugin.pk = None
                    plugin.id = None
                    plugin.parent = article
                    plugin.save()

            copy_plugins(models.RichText)
            copy_plugins(models.Image)
            copy_plugins(models.HTML)
            copy_plugins(models.External)
    copy_selected.short_description = _("copy selected")


@admin.register(NameSpace)
class NamespaceAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]

    list_display = [
        'name',
        'slug',
        'language_code'
    ]

    list_filter = [
        'language_code'
    ]

    prepopulated_fields = {
        "slug": ("name",)
    }

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'language_code')
        }),
    )
