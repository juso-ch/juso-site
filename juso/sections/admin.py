from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from feincms3.admin import TreeAdmin
from feincms3_meta.models import MetaMixin
from reversion.admin import VersionAdmin

from juso.sections.models import Category, Section

# Register your models here.


@admin.register(Section)
class SectionAdmin(VersionAdmin, TreeAdmin):
    list_display = [
        "indented_title",
        "move_column",
        "name",
    ]

    autocomplete_fields = ["site", "parent"]

    prepopulated_fields = {
        "slug": ("name", ),
    }

    filter_horizontal = ["users"]

    fieldsets = (
        (None, {
            "fields": ("name", "users", "parent")
        }),
        (_("advanced"), {
            "classes": ("collapse", ),
            "fields": ("slug", "site")
        }),
    )

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        if request.user.is_superuser:
            return True
        sections = request.user.section_set.all()
        return obj in sections

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)

        if request.user.is_superuser:
            return True

        sections = request.user.section_set.all()
        return obj in sections

    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(VersionAdmin, TreeAdmin):
    list_display = [
        "indented_title",
        "move_column",
        "name",
        "slug",
        "parent",
        "language_code",
    ]
    list_filter = ["language_code"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name", )}

    autocomplete_fields = ["parent", "translations"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "language_code",
                    "parent",
                    "header_image",
                    "header_image_ppoi",
                    "color",
                )
            },
        ),
        MetaMixin.admin_fieldset(),
        (
            _("translations"),
            {
                "classes": ("collapse", ),
                "fields": ("translations", ),
            },
        ),
    )
