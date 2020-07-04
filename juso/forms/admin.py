import csv

from content_editor.admin import ContentEditor, ContentEditorInline
from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from reversion.admin import VersionAdmin
# Register your models here.

from juso.forms.models import Form, FormField
from juso.sections.models import Section
from juso.utils import CopyContentMixin


class FormFieldInline(ContentEditorInline):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "slug", "input_type", "required"),
                    "ordering",
                    "region",
                )
            },
        ),
        (
            _("advanced"),
            {
                "classes": ("collapse",),
                "fields": (
                    "size",
                    "choices",
                    "initial",
                    "help_text",
                    "unique",
                    "unique_error",
                ),
            },
        ),
    )


@admin.register(Form)
class FormAdmin(VersionAdmin, ContentEditor, CopyContentMixin):
    list_display = [
        "title",
        "slug",
        "created_date",
        "section",
        "language_code",
        "count",
    ]

    list_filter = [
        "section",
        "language_code",
    ]

    autocomplete_fields = ["section"]

    search_fields = [
        "title",
    ]

    prepopulated_fields = {
        "slug": ("title",),
    }

    readonly_fields = (
        "created_date",
        "edited_date",
    )

    fieldsets = (
        (
            None,
            {"fields": ("title", "slug", "section", "created_date", "edited_date",)},
        ),
        (
            _("settings"),
            {
                "classes": ("tabbed",),
                "fields": (
                    "submit",
                    "size",
                    "success_message",
                    "success_redirect",
                    "webhook",
                    "email",
                    "fullwidth",
                ),
            },
        ),
        (
            _("meta"),
            {
                "classes": ("tabbed",),
                "fields": (
                    "meta_title",
                    "meta_author",
                    "meta_description",
                    "meta_image",
                    "meta_image_ppoi",
                    "meta_robots",
                    "meta_canonical",
                ),
            },
        ),
        (_("translations"), {"classes": ("tabbed",), "fields": ("translations",)}),
    )

    actions = ["export_form"]

    inlines = [
        FormFieldInline.create(FormField),
    ]

    plugins = [FormField]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if "section" not in form.base_fields:
            return form

        section_field = form.base_fields["section"]

        sections = request.user.section_set.all()
        section_field.initial = sections[0]

        return form

    def has_delete_permission(self, request, obj=None):
        if obj is None or request.user.is_superuser:
            return super().has_change_permission(request, obj)
        sections = request.user.section_set.all()
        return obj.section in sections

    def has_change_permission(self, request, obj=None):
        if obj is None or request.user.is_superuser:
            return super().has_change_permission(request, obj)
        sections = request.user.section_set.all()
        return obj.section in sections

    def export_form(self, request, query):

        form = query.first()

        if form.section not in Section.objects.filter(users=request.user):
            messages.add_message(request, messages.ERROR, _("access denied"))
            return

        entries, fields = form.entry_dict()

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="somefilename.csv"'

        writer = csv.DictWriter(response, fieldnames=fields)
        writer.writeheader()
        writer.writerows(entries)

        return response
