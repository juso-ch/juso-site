import json
import urllib
import uuid

import bleach
import pytz
from content_editor.models import Region, create_plugin_base
from django.conf import settings
from django.db import models
from django.urls import NoReverseMatch
from django.utils import timezone
from django.utils.timezone import datetime, now
from django.utils.translation import gettext_lazy as _
from feincms3 import plugins
from feincms3.apps import apps_urlconf, reverse_app
from feincms3_meta.models import MetaMixin
from feincms3_sites.middleware import current_site, set_current_site
from imagefield.fields import ImageField
from taggit.managers import TaggableManager

from juso.blog import plugins as blog_plugins
from juso.events import plugins as event_plugins
from juso.forms import plugins as form_plugins
from juso.models import Button, TranslationMixin
from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.sections.models import ContentMixin, Section, get_template_list

# Create your models here.


class Location(MetaMixin, TranslationMixin):
    regions = [Region(key="images", title=_("images"))]
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField(unique=True)

    street = models.CharField(max_length=200, verbose_name=_("street"))
    city = models.CharField(max_length=100, verbose_name=_("city"))
    zip_code = models.CharField(max_length=20, verbose_name=_("zip code"))
    country = models.CharField(max_length=200, verbose_name=_("country"))
    is_physical = models.BooleanField(verbose_name=_("is physical"), default=True,)

    header_image = ImageField(
        _("header image"),
        formats={
            "full": ["default", "darken", ("crop", (1920, 900))],
            "mobile": ["default", ("crop", (740, 600))],
        },
        auto_add_fields=True,
        blank=True,
        null=True,
    )

    section = models.ForeignKey(
        Section, models.SET_NULL, blank=True, null=True, verbose_name=_("section")
    )

    website = models.URLField(blank=True, verbose_name=_("website"))

    lng = models.FloatField(verbose_name=_("longitude"), default=0)
    lat = models.FloatField(verbose_name=_("latitude"), default=0)

    tags = TaggableManager(blank=True)

    def maps(self):
        return settings.MAPS_URL.format(location=self)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

    @property
    def address(self):
        return f"{self.street}, {self.zip_code} {self.city}"

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        ordering = ["name"]

    def get_absolute_url(self):
        try:
            site = current_site()
            if not self.section or site == self.section.site:
                return reverse_app(
                    [f"{site.pk}-events"], "location-detail", kwargs={"slug": self.slug}
                )
            with set_current_site(self.section.site):
                return (
                    "//"
                    + self.section.site.host
                    + reverse_app(
                        [f"{self.section.site.id}-events"],
                        "location-detail",
                        urlconf=apps_urlconf(),
                        kwargs={"slug": self.slug},
                    )
                )
        except NoReverseMatch:
            return "#"


LocationPluginBase = create_plugin_base(Location)


class LocationImage(plugins.image.Image, LocationPluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)


def ical_calendar(queryset):
    begin = (
        "BEGIN:VCALENDAR\r\n" "VERSION:2.0\r\n" "METHOD:PUBLISH\r\n" "PRODID:JUSO\r\n"
    )
    events = "".join(e.ical_event() for e in queryset)
    return begin + events + "END:VCALENDAR\r\n"


class Event(ContentMixin):
    TEMPLATES = get_template_list("events", (("default", ("main",),),))

    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))
    slug = models.SlugField(max_length=180)
    uuid = models.UUIDField(default=uuid.uuid4)

    location = models.ForeignKey(
        Location, models.SET_NULL, blank=True, null=True, verbose_name=_("location")
    )

    @property
    def description(self):
        return self.meta_description or self.tagline[:300]

    @property
    def tagline(self):
        if RichText.objects.filter(parent=self).exists():
            return bleach.clean(
                RichText.objects.filter(parent=self)[0].text, strip=True, tags=[],
            )
        if self.meta_description:
            return self.meta_description
        return ""

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ["start_date"]
        indexes = [models.Index(fields=["start_date", "slug", "section"])]
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "start_date", "section"],
                name="unique_slugs_for_section_and_date",
            )
        ]

    def webpush_data(self, page):
        if favicon := page.top_page().favicon:
            icon = f"https://{page.site.host}" + favicon["512"]
        else:
            icon = "https://" + page.site.host + "/static/logo.png"
        return json.dumps(
            {
                "title": self.start_date.astimezone(
                    pytz.timezone(settings.TIME_ZONE)
                ).strftime("%d.%m.%Y %H:%M")
                + " - "
                + self.title,
                "tagline": (self.location.name + "; " if self.location else "")
                + self.tagline[:280],
                "icon": icon,
                "url": self.get_full_url(),
                "badge": "https://" + page.site.host + "/static/badge.png",
                "publication_date": self.publication_date.isoformat(),
                "image": "https://" + page.site.host + self.get_header_image().full
                if self.get_header_image()
                else "",
            }
        )

    def get_full_url(self):
        url = self.get_absolute_url()
        if url.startswith("//"):
            return "https:" + url
        else:
            return "https://" + self.section.site.host + url

    def get_address(self):
        if self.location:
            return self.location.address + ", " + self.location.country
        return ""

    def google_calendar(self):
        start = self.start_date.strftime("%Y%m%dT%H%M00")
        end = self.end_date.strftime("%Y%m%dT%H%M00")
        query = urllib.parse.urlencode(
            {
                "action": "TEMPLATE",
                "dates": f"{start}/{end}",
                "text": f"{self.title} ({self.section.name})",
                "location": self.get_address(),
                "details": f"https://{self.section.site.host}{self.get_absolute_url()}",
            }
        )
        return f"https://www.google.com/calendar/render?{query}"

    def outlook(self):
        start = self.start_date.strftime("%Y%m%dT%H%M00")
        end = self.end_date.strftime("%Y%m%dT%H%M00")
        query = urllib.parse.urlencode(
            {
                "path": "/calendar/action/compose",
                "rru": "addevent",
                "startdt": start,
                "enddt": end,
                "subject": f"{self.title} ({self.section.name})",
                "location": self.get_address(),
                "body": f"https://{self.section.site.host}{self.get_absolute_url()}",
            }
        )
        return f"https://outlook.live.com/owa/?{query}"

    def ical_link(self):
        return "data:text/calendar;charset=utf8," + urllib.parse.quote(
            ical_calendar([self])
        )

    def ical_event(self):
        start = self.start_date.strftime("%Y%m%dT%H%M00")
        end = self.end_date.strftime("%Y%m%dT%H%M00")
        timestamp = now().strftime("%Y%m%dT%H%M00")
        return (
            "BEGIN:VEVENT\r\n"
            f"UID:{self.uuid}\r\n"
            f"DTSTAMP:{timestamp}Z\r\n"
            f"SUMMARY:{self.title}\r\n"
            f"DTSTART:{start}Z\r\n"
            f"DTEND:{end}Z\r\n"
            f"DESCRIPTION:https://{self.section.site.host}{self.get_absolute_url()}\r\n"
            f"LOCATION:{self.get_address()}\r\n"
            "END:VEVENT\r\n"
        )

    def get_absolute_url(self):
        try:
            site = current_site()
            if site == self.section.site:
                return reverse_app(
                    [f"{site.id}-events-{self.category}", f"{site.id}-events",],
                    "event-detail",
                    kwargs={
                        "slug": self.slug,
                        "day": self.start_date.day,
                        "month": self.start_date.month,
                        "year": self.start_date.year,
                    },
                    languages=[self.language_code],
                )
            with set_current_site(self.section.site):
                return (
                    "//"
                    + self.section.site.host
                    + reverse_app(
                        [
                            f"{self.section.site.id}-events-{self.category}",
                            f"{self.section.site.id}-events",
                        ],
                        "event-detail",
                        urlconf=apps_urlconf(),
                        kwargs={
                            "slug": self.slug,
                            "day": self.start_date.day,
                            "month": self.start_date.month,
                            "year": self.start_date.year,
                        },
                        languages=[self.language_code],
                    )
                )
        except NoReverseMatch:
            return "#"


PluginBase = create_plugin_base(Event)


class External(plugins.external.External, PluginBase):
    pass


class RichText(plugins.richtext.RichText, PluginBase):
    pass


class Image(plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)
    title = models.CharField(_("title"), max_length=200, blank=True)
    fullwidth = models.BooleanField(_("full width"), default=False)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")


class HTML(plugins.html.HTML, PluginBase):
    pass


class Download(download.Download, PluginBase):
    pass


class Team(people_plugins.TeamPlugin, PluginBase):
    pass


class CandidaturePlugin(people_plugins.CandidatePlugin, PluginBase):
    pass


class Button(Button, PluginBase):
    pass


class ArticlePlugin(blog_plugins.ArticlePlugin, PluginBase):
    pass


class EventPlugin(event_plugins.EventPlugin, PluginBase):
    pass


class FormPlugin(form_plugins.FormPlugin, PluginBase):
    pass


class FormEntryCounterPlugin(form_plugins.EntryCounter, PluginBase):
    pass


plugins = [
    RichText,
    Image,
    HTML,
    External,
    Team,
    Download,
    Button,
    ArticlePlugin,
    EventPlugin,
    FormPlugin,
    CandidaturePlugin,
]
