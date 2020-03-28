from django.template.loader import render_to_string
from django.utils.html import mark_safe
from django.utils.translation import gettext as _
from feincms3.plugins.external import oembed_html, oembed_json


def copy_plugins(model_class, old_parent, parent):
    for plugin in model_class.objects.filter(parent=old_parent):
        plugin.pk = None
        plugin.id = None
        plugin.parent = parent
        plugin.save()


class CopyContentMixin():

    plugins = []

    def copy_selected(self, request, queryset):
        duplicated = []
        for page in queryset.all():

            if page.pk in duplicated:
                continue

            page.slug = page.slug + '-copy'
            parent = self.copy_descendants(page, duplicated)
            parent.save()

    def copy_descendants(self, old_parent, duplicated):
        old_pk = old_parent.pk
        parent = old_parent
        parent.pk = None
        parent.id = None
        parent.save()

        duplicated.append(old_pk)

        old_parent = type(parent).objects.get(pk=old_pk)

        for plugin in self.plugins:
            copy_plugins(plugin, old_parent, parent)

        if not hasattr(old_parent, "children"):
            return parent

        for child in old_parent.children.all():
            new_child = self.copy_descendants(child, duplicated)
            new_child.parent = parent
            new_child.save()

        return parent

    copy_selected.short_description = _("copy selected")


meta_fieldset = (_('meta'), {
    'classes': ('tabbed',),
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


def render_embed(plugin, **kwargs):
    return render_to_string('plugins/embed.html', {
        'json': oembed_json(plugin.url),
        'html': mark_safe(oembed_html(plugin.url)),
    })


number_words = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven'
}


def number_word(number):
    if number in number_words.keys():
        return number_words[number]
    return ''
