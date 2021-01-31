from content_editor.admin import ContentEditor
from django.conf import settings
from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from feincms3 import plugins
from feincms3_meta.models import MetaMixin
from geopy.geocoders import Nominatim
from js_asset import JS
from reversion.admin import VersionAdmin

from juso.admin import ButtonInline
from juso.blog import plugins as blog_plugins
from juso.events import models
from juso.events import plugins as event_plugins
from juso.events.models import Event, Location
from juso.forms import plugins as form_plugins
from juso.pages.models import Page
from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.utils import CopyContentMixin
from juso.webpush import models as webpush
from juso.webpush import tasks

# Register your models here.


@admin.register(Event)
class EventAdmin(VersionAdmin, ContentEditor, CopyContentMixin):
    list_display = [
        "title",
        "slug",
        "start_date",
        "language_code",
    ]

    list_filter = [
        "category",
        "language_code",
        "section",
    ]

    search_fields = [
        "title",
    ]

    date_hierarchy = "start_date"

    autocomplete_fields = [
        "category",
        "author",
        "section",
        "location",
        "translations",
    ]

    prepopulated_fields = {
        "slug": ("title", ),
    }

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "author",
                    (
                        "start_date",
                        "end_date",
                    ),
                    "location",
                    "category",
                    "tags",
                    "header_image",
                    "header_image_ppoi",
                )
            },
        ),
        (
            _("settings"),
            {
                "classes": ("collapse", ),
                "fields": (
                    "language_code",
                    "slug",
                    "section",
                    "template_key",
                ),
            },
        ),
        MetaMixin.admin_fieldset(),
        (_("translations"), {
            "classes": ("tabbed", ),
            "fields": ("translations", )
        }),
    )

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External),
        download.DownloadInline.create(models.Download),
        people_plugins.TeamPluginInline.create(models.Team),
        people_plugins.CandidateListPluginInline.create(
            models.CandidaturePlugin),
        blog_plugins.ArticlePluginInline.create(models.ArticlePlugin),
        event_plugins.EventPluginInline.create(models.EventPlugin),
        ButtonInline.create(models.Button),
        form_plugins.FormPluginInline.create(models.FormPlugin),
    ]

    plugins = models.plugins

    actions = ["copy_selected", "send_webpush"]

    plugins = models.plugins

    class Media:
        js = (
            "admin/js/jquery.init.js",
            JS(
                "https://kit.fontawesome.com/7655daeee1.js",
                {
                    "async": "async",
                    "crossorigin": "anonymous",
                },
                static=False,
            ),
            "admin/plugin_buttons.js",
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        section_field = form.base_fields["section"]

        sections = request.user.section_set.all()
        section_field.initial = sections[0]

        return form

    def send_webpush(self, request, queryset):
        for event in queryset:
            pages = Page.objects.filter(
                (Q(application="events")
                 & Q(language_code=event.language_code))
                & (Q(category__isnull=True) | Q(category=event.category))
                & (Q(site__section=event.section) | Q(sections=event.section)))

            for page in pages:
                subscriptions = webpush.Subscription.objects.filter(page=page)
                data = event.webpush_data(page)
                for subscription in subscriptions:
                    tasks.send_data_to.delay(data, subscription.pk)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(section__in=sections)


@admin.register(Location)
class LocationAdmin(VersionAdmin, ContentEditor):
    search_fields = [
        "name",
        "street",
        "city",
    ]

    list_display = [
        "name",
        "slug",
        "street",
        "city",
        "lng",
        "lat",
    ]

    list_filter = ["city"]

    prepopulated_fields = {"slug": ("name", )}

    autocomplete_fields = ["section", "translations"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "street",
                    (
                        "city",
                        "zip_code",
                    ),
                    "country",
                )
            },
        ),
        (
            _("advanced"),
            {
                "classes": ("tabbed", ),
                "fields": (
                    "section",
                    "slug",
                    "is_physical",
                    "lat",
                    "lng",
                    "header_image",
                    "header_image_ppoi",
                ),
            },
        ),
        MetaMixin.admin_fieldset(),
        (_("translations"), {
            "classes": ("tabbed", ),
            "fields": ("translations", )
        }),
    )

    inlines = [
        plugins.image.ImageInline.create(models.LocationImage),
    ]

    def has_change_permission(self, request, obj=None):
        if obj is None or obj.section is None:
            return super().has_change_permission(request, obj)
        sections = request.user.section_set.all()
        return obj.section in sections

    def save_model(self, request, obj, form, change):
        if not change and obj.is_physical:
            locator = Nominatim(user_agent=settings.NOMINATIM_USER_AGENT)
            location = locator.geocode(
                f"{obj.street}, {obj.zip_code} {obj.city}, {obj.country}")
            if location:
                obj.lat = location.latitude
                obj.lng = location.longitude
        super().save_model(request, obj, form, change)
