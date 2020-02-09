from django.contrib import admin

# Register your models here.

from feincms3_sites.models import Site
from content_editor.admin import ContentEditor

from feincms3 import plugins

from feincms3.admin import TreeAdmin

from juso.pages import models
from js_asset import JS


class PageAdmin(ContentEditor, TreeAdmin):
    list_display = [
        "indented_title",
        "move_column",
        "is_active", 'menu',
        'language_code',
        "template_key",
        'application',
    ]
    actions = ['copy_selected']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active']

    raw_id_fields = ['parent']

    list_filter = ['is_active', 'menu']

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External)
    ]

    mptt_level_indent = 30

    class Media:
        js = (
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

        if request.user.is_superuser:
            return form

        sections = request.user.section_set.all()
        site_field.queryset = Site.objects.filter(section__in=sections)
        site_field.initial = Site.objects.filter(section__in=sections)[0]

        if site_field.queryset.count() == 1:
            site_field.disabled = True

        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(site__section__in=sections)

    def copy_selected(self, request, queryset):
        duplicated = []
        for page in queryset.all():
            # Skip
            if page.pk in duplicated:
                continue
            page.path = page.path + 'copy/'
            parent = self.copy_descendants(page, duplicated)
            parent.save()

    def copy_descendants(self, old_parent, duplicated):

        old_pk = old_parent.pk
        parent = old_parent
        parent.pk = None
        parent.id = None
        parent.save()

        duplicated.append(old_pk)

        old_parent = models.Page.objects.get(pk=old_pk)

        def copy_plugins(model_class):
            for plugin in model_class.objects.filter(parent=old_parent):
                plugin.pk = None
                plugin.id = None
                plugin.parent = parent
                plugin.save()

        copy_plugins(models.RichText)
        copy_plugins(models.Image)
        copy_plugins(models.HTML)
        copy_plugins(models.External)

        for child in old_parent.descendants().all():
            new_child = self.copy_descendants(child, duplicated)
            new_child.parent = parent
            new_child.save()

        return parent


admin.site.register(models.Page, PageAdmin)
