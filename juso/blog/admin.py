from django.contrib import admin

from feincms3 import plugins
from juso.blog.models import Article, NameSpace
from content_editor.admin import ContentEditor

from juso.blog import models
from js_asset import JS
# Register your models here.


@admin.register(Article)
class ArticleAdmin(ContentEditor):
    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External)
    ]

    class Media:
        js = (
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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        section_field = form.base_fields['section']

        if not request.user.is_superuser:
            sections = request.user.section_set.all()
        section_field.queryset = sections
        section_field.initial = sections[0]

        if section_field.queryset.count() == 1:
            section_field.disabled = True

        return form


@admin.register(NameSpace)
class NamespaceAdmin(admin.ModelAdmin):
    pass
