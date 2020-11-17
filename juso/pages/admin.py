from admin_ordering.admin import OrderableAdmin
from content_editor.admin import ContentEditor, ContentEditorInline
from django import forms
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect, render, reverse
from django.urls import path
from django.utils.translation import gettext_lazy as _, pgettext
from django.utils.html import format_html, mark_safe
from feincms3 import plugins
from feincms3.admin import TreeAdmin, MoveForm
from feincms3_meta.models import MetaMixin
from feincms3_sites.admin import SiteAdmin
from feincms3_sites.models import Site
from feincms3_sites.middleware import current_site
from js_asset import JS
from reversion.admin import VersionAdmin
from tree_queries.forms import TreeNodeChoiceField

from juso.admin import ButtonInline, VotingRecommendationInline
from juso.blog import plugins as blog_plugins
from juso.events import plugins as event_plugins
from juso.forms import plugins as form_plugins
from juso.glossary.admin import GlossaryContentInline
from juso.pages import models
from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.utils import CopyContentMixin

# Register your models here.


class CategoryLinkingInline(OrderableAdmin, admin.TabularInline):
    model = models.CategoryLinking
    fk_name = "page"

    ordering_field = "order"
    ordering_field_hide_input = True

    autocomplete_fields = ["category", "other_site"]


class NavigationPluginInline(ContentEditorInline):
    autocomplete_fields = ["pages"]


class PageAdmin(VersionAdmin, CopyContentMixin, ContentEditor, TreeAdmin):
    list_display = [
        "indented_title",
        "move_column",
        "path",
        "is_active",
        "language_code",
        "application",
    ]
    actions = ["open_duplicate_form"]

    list_per_page = 50

    prepopulated_fields = {"slug": ("title",)}

    autocomplete_fields = [
        "site",
        "parent",
        "blog_namespace",
        "category",
        "redirect_to_page",
        "translations",
        "featured_categories",
        "sections",
        "collection",
    ]

    search_fields = ["title"]
    list_editable = []

    list_filter = ["is_active", "menu", "language_code", "site"]

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External),
        download.DownloadInline.create(models.Download),
        ButtonInline.create(models.Button),
        VotingRecommendationInline.create(models.VotingRecommendationPlugin),
        people_plugins.TeamPluginInline.create(models.Team),
        people_plugins.CandidateListPluginInline.create(models.CandidaturePlugin),
        event_plugins.EventPluginInline.create(models.EventPlugin),
        blog_plugins.ArticlePluginInline.create(models.ArticlePlugin),
        GlossaryContentInline.create(models.GlossaryRichText),
        form_plugins.FormPluginInline.create(models.FormPlugin),
        form_plugins.EntryCounterInline.create(models.FormEntryCounterPlugin),
        NavigationPluginInline.create(models.NavigationPlugin),
        CategoryLinkingInline,
    ]

    plugins = models.plugins
    readonly_fields = ["app_instance_namespace"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "parent",
                )
            },
        ),
        (
            _("settings"),
            {
                "fields": (
                    "is_active",
                    "menu",
                    "language_code",
                    "template_key",
                    "is_landing_page",
                    "header_image",
                    "header_image_ppoi",
                ),
            },
        ),
        (
            _("path"),
            {
                "classes": ("tabbed",),
                "fields": (
                    "slug",
                    "static_path",
                    "path",
                    "site",
                ),
            },
        ),
        (
            _("application"),
            {
                "classes": ("tabbed",),
                "fields": (
                    "application",
                    "category",
                    "blog_namespace",
                    "featured_categories",
                    "sections",
                    "collection",
                    "app_instance_namespace",
                ),
            },
        ),
        MetaMixin.admin_fieldset(),
        (
            _("redirect"),
            {
                "classes": ("tabbed",),
                "fields": (
                    "redirect_to_page",
                    "redirect_to_url",
                ),
            },
        ),
        (_("translations"), {"classes": ("tabbed",), "fields": ("translations",)}),
        (
            _("advanced"),
            {
                "classes": ("tabbed",),
                "fields": (
                    "in_meta",
                    "is_navigation",
                    "position",
                    "logo",
                    "favicon",
                    "primary_color",
                    "css_vars",
                    "fonts",
                    "prefetches",
                    "google_site_verification",
                ),
            },
        ),
    )

    mptt_level_indent = 30

    def move_view(self, request, obj):
        return self.action_form_view(
            request, obj, form_class=ResctrictedMoveForm, title=_("Move %s") % obj
        )

    class Media:
        js = (
            "admin/js/jquery.init.js",
            JS(
                "https://kit.fontawesome.com/91a6274901.js",
                {
                    "async": "async",
                    "crossorigin": "anonymous",
                },
                static=False,
            ),
            "admin/plugin_buttons.js",
        )

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if (
            hasattr(obj, "pk")
            and models.Page.objects.get(pk=obj.pk).application == "categories"
        ):
            return inlines
        return inlines[:-1]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        site_field = form.base_fields["site"]
        site_field.required = True

        sections = request.user.section_set.all()
        site_field.initial = Site.objects.filter(section__in=sections)[0]

        return form

    def indented_title(self, instance):
        """
        Use Unicode box-drawing characters to visualize the tree hierarchy.
        """
        box_drawing = []
        for i in range(instance.tree_depth - 1):
            box_drawing.append('<i class="l"></i>')
        if instance.tree_depth > 0:
            box_drawing.append('<i class="a"></i>')

        return format_html(
            '<div class="box">'
            '<div class="box-drawing">{}</div>'
            '<div class="box-text" style="text-indent:{}px">{}</div>'
            "</div>",
            mark_safe("".join(box_drawing)),
            instance.tree_depth * 30,
            instance.title,
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(site__section__in=sections)

    def open_duplicate_form(self, request, queryset):
        return redirect(
            reverse(
                "admin:pages_Page_duplicate_page_tree",
                kwargs={"pk": queryset[0].pk},
            )
        )

    open_duplicate_form.short_description = _("Duplicate page-tree")

    def get_urls(self):
        urls = super().get_urls()
        return [
            path(
                "<int:pk>/duplicate/",
                self.admin_site.admin_view(self.duplicate_page_tree),
                name="pages_Page_duplicate_page_tree",
            )
        ] + urls

    def duplicate_page_tree(self, request, pk):
        page = models.Page.objects.get(pk=pk)
        form = DuplicateForm(page=page, request=request)
        if request.method == "POST":
            form = DuplicateForm(request.POST, page=page, request=request)

            if form.is_valid():
                old_pk = page.pk
                new_root = page
                language_code = form.cleaned_data["language_code"]
                site = form.cleaned_data["site"]
                link_translations = form.cleaned_data["link_translations"]
                children = page.children.all()

                new_root.pk = None
                new_root.language_code = language_code
                new_root.site = site
                new_root.slug = form.cleaned_data["new_slug"]
                new_root.path = form.cleaned_data["new_path"]
                new_root.static_path = True
                new_root.title = form.cleaned_data["new_title"]
                new_root.save()

                if link_translations:
                    new_root.translations.add(old_pk)
                    new_root.save()

                def copy_children(page, children):
                    for child in children:
                        new_children = child.children.all()
                        child.parent = page
                        old_pk = child.pk
                        child.pk = None
                        child.language_code = language_code
                        child.site = site
                        child.save()
                        if link_translations:
                            child.translations.add(old_pk)
                            child.save()
                        copy_children(child, new_children)

                copy_children(new_root, children)

                return redirect("admin:pages_page_changelist")
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            title=_("Duplicate Page-Tree"),
            app_label="pages",
            opts=models.Page._meta,
            model=models.Page,
        )

        return render(request, "admin/duplicate_page_tree.html", context)


class DuplicateForm(forms.Form):

    language_code = forms.ChoiceField(choices=settings.LANGUAGES)
    site = forms.ModelChoiceField(Site.objects.all())
    new_slug = forms.CharField()
    new_path = forms.CharField()
    new_title = forms.CharField()
    link_translations = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop("page")
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        if self.request.user.is_superuser:
            return

        self.fields["site"].queryset = Site.objects.filter(
            section__in=self.request.user.section_set.all()
        )


class SiteAdmin(SiteAdmin):
    search_fields = ["host"]

    list_editable = [
        "default_language",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(section__in=sections)


class ResctrictedMoveForm(MoveForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = self.model._default_manager.filter(
            site=self.instance.site
        ).with_tree_fields()

        self.fields["of"] = TreeNodeChoiceField(
            label=pgettext("MoveForm", "Of"),
            required=False,
            queryset=queryset.exclude(pk__in=queryset.descendants(self.instance)),
            label_from_instance=lambda obj: "{}{}".format(
                "".join(["*** " if obj == self.instance else "--- "] * obj.tree_depth),
                obj,
            ),
        )
        self.fields["of"].widget.attrs.update({"size": 30, "style": "height:auto"})


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
admin.site.register(models.Page, PageAdmin)

admin.site.site_header = _("JUSO Schweiz")
admin.site.site_title = _("JUSO Admin")
