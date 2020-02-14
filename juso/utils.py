from django.utils.translation import gettext as _


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

        old_parent = type(parent).objects.get(pk=old_pk)

        for plugin in self.plugins:
            copy_plugins(plugin, old_parent, parent)

        for child in old_parent.children.all():
            new_child = self.copy_descendants(child, duplicated)
            new_child.parent = parent
            new_child.save()

        return parent

    copy_selected.short_description = _("copy selected")
