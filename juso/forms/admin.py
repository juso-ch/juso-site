import csv
import json
from datetime import datetime

import xlsxwriter
from content_editor.admin import ContentEditor, ContentEditorInline
from admin_ordering.admin import OrderableAdmin
from django import forms
from django.contrib import admin, messages
from django.contrib.auth.decorators import user_passes_test
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.urls import path
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from flat_json_widget.widgets import FlatJsonWidget
from js_asset import JS
from reversion.admin import VersionAdmin

from juso.forms.models import (
    Form,
    FormField,
    MailchimpConnection,
    FormEntry,
    FormEntryValue,
    Webhook,
    WebhookField,
)
from juso.sections.models import Section
from juso.utils import CopyContentMixin

# Register your models here.


class FormFieldInline(OrderableAdmin, admin.StackedInline):
    model = FormField
    ordering_field = "ordering"
    ordering_field_hide_input = True
    fieldsets = ((
        None,
        {
            "fields": (
                ("name", "slug", "ordering"),
                ("input_type", "required", "unique"),
                ("size", "initial", "help_text"),
                ("choices", "unique_error", "disallow_text"),
            ),
        },
    ), )


class FormEntryValueInline(admin.TabularInline):
    model = FormEntryValue

    fields = ["field", "value"]

    can_delete = False

    readonly_fields = ["field"]

    formfield_overrides = {models.TextField: {"widget": forms.TextInput}}

    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(FormEntry)
class FormEntryAdmin(admin.ModelAdmin):
    list_display = [
        "submission_id",
        "ip",
        "created",
        "form",
    ]

    readonly_fields = ["form", "ip", "submission_id"]

    search_fields = [
        "fields__value",
        "ip",
    ]

    list_filter = [
        "form",
    ]

    inlines = [FormEntryValueInline]

    ordering = ["created"]

    date_hierarchy = "created"

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        sections = request.user.section_set.all()
        return super().get_queryset(request).filter(form__section__in=sections)


@admin.register(Form)
class FormAdmin(VersionAdmin, CopyContentMixin):
    list_display = [
        "title",
        "slug",
        "created_date",
        "section",
        "language_code",
        "result_link",
    ]

    list_filter = [
        "section",
        "language_code",
    ]

    autocomplete_fields = ["section", "mailchimp_connection", "webhooks"]

    search_fields = [
        "title",
    ]

    prepopulated_fields = {
        "slug": ("title", ),
    }

    readonly_fields = (
        "created_date",
        "edited_date",
    )

    formfield_overrides = {
        models.JSONField: {
            "widget": FlatJsonWidget
        },
    }

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "section",
                    "created_date",
                    "edited_date",
                )
            },
        ),
        (
            _("settings"),
            {
                "classes": ("tabbed", ),
                "fields": (
                    "submit",
                    "size",
                    "success_message",
                    "success_redirect",
                    "fullwidth",
                ),
            },
        ),
        (
            _("collection"),
            {
                "classes": ("tabbed", ),
                "fields": (
                    "email",
                    "list_id",
                    "webhooks",
                    "mailchimp_connection",
                    "mailchimp_list_id",
                    "tags",
                ),
            },
        ),
        (
            _("advanced"),
            {
                "classes": ("tabbed", ),
                "fields": (
                    "linked_form",
                    "linking_field_slug",
                ),
            },
        ),
        (
            _("meta"),
            {
                "classes": ("tabbed", ),
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
    )

    actions = ["export_form", "clear_form", "export_form_xlsx"]

    inlines = [
        FormFieldInline,
    ]

    plugins = [FormField]

    class Media:
        js = ("content_editor/tabbed_fieldsets.js", )
        css = {"all": ["content_editor/content_editor.css"]}

    def result_link(self, obj):
        url = reverse("admin:forms_Form_show_results", args=(obj.pk, ))
        return mark_safe(f'<a href="{url}">{obj.count()}</a>')

    result_link.short_description = _("results")

    def get_urls(self):
        urls = super().get_urls()
        return [
            path(
                "results/<int:pk>/",
                user_passes_test(
                    lambda user: user.is_staff, login_url="/admin/login/")(
                        self.admin_site.admin_view(self.show_results)),
                name="forms_Form_show_results",
            )
        ] + urls

    def show_results(self, request, pk):
        form = Form.objects.get(pk=pk)
        if not self.can_access_entries(form, request):
            return redirect("admin:forms_form_changelist")

        entries, fields = form.entry_dict()

        context = dict(
            self.admin_site.each_context(request),
            form=form,
            title=_("Display results"),
            app_label="auth",
            opts=Form._meta,
            model=Form,
            fields=fields,
            entries=entries,
            data=entries,
            original=form,
            has_view_permission=True,
        )

        return render(request, "admin/form_results.html", context)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)

        if obj is None or request.user.is_superuser:
            return super().get_fieldsets(request, obj=obj)

        sections = request.user.section_set.all()
        if obj.section in sections:
            return super().get_fieldsets(request, obj=obj)
        return ((
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "section",
                    "created_date",
                    "edited_date",
                )
            },
        ), )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if "section" not in form.base_fields:
            return form

        section_field = form.base_fields["section"]
        #        form.base_fields["list_id"].widget = forms.PasswordInput()

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

    def can_access_entries(self, form, request):
        if form.section not in Section.objects.filter(users=request.user):
            messages.add_message(request, messages.ERROR, _("access denied"))
            return False
        return True

    def export_form(self, request, query):

        form = query.first()

        if not self.can_access_entries(form, request):
            return

        entries, fields = form.entry_dict()

        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"] = f'attachment; filename="{form.slug}-{timezone.now():%Y%m%d%H%M}.csv"'

        writer = csv.DictWriter(response, fieldnames=fields)
        writer.writeheader()
        writer.writerows(entries)

        return response

    def export_form_xlsx(self, request, query):

        response = HttpResponse(
            content_type=
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        response[
            "Content-Disposition"] = f'attachment; filename="form-export-{timezone.now():%Y%m%d%H%M}.xlsx"'

        workbook = xlsxwriter.Workbook(response, {"remove_timezone": True})
        bold = workbook.add_format({"bold": True})
        date_format = workbook.add_format({"num_format": "yy-mm-dd hh:mm"})

        for form in query.all():

            if not self.can_access_entries(form, request):
                continue

            worksheet = workbook.add_worksheet(f"answers-{form.slug}")
            entries, fields = form.entry_dict()

            for col, field in enumerate(fields):
                worksheet.write(0, col, field, bold)

            for row, entry in enumerate(entries):
                for col, field in enumerate(fields):
                    val = entry.get(field, "")
                    if isinstance(val, datetime):
                        worksheet.write(row + 1, col, entry.get(field, ""),
                                        date_format)
                    else:
                        worksheet.write(row + 1, col, entry.get(field, ""))

        workbook.close()

        return response

    def clear_form(self, request, query):
        form = query.first()
        response = self.export_form_xlsx(request, query)

        if response:
            form.clear_entries()

        return response


@admin.register(MailchimpConnection)
class MailchimpConnectionAdmin(admin.ModelAdmin):

    list_display = ("name", "section", "api_server")

    search_fields = ("name", "section")

    autocomplete_fields = ("section", )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        sections = request.user.section_set.all()
        return super().get_queryset(request).filter(section__in=sections)


class WebhookFieldInline(admin.TabularInline):
    model = WebhookField


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")

    search_fields = ("name", )

    autocomplete_fields = ("owner", )

    inlines = [WebhookFieldInline]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        sections = request.user.section_set.all()
        return super().get_queryset(request).filter(onwer__in=sections)
