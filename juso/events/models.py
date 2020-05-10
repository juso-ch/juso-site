from content_editor.models import Region, create_plugin_base
from django.db import models
from django.utils.translation import gettext as _
from feincms3 import plugins
from feincms3.apps import apps_urlconf, reverse_app
from feincms3_meta.models import MetaMixin
from feincms3_sites.middleware import current_site, set_current_site
from taggit.managers import TaggableManager
from imagefield.fields import ImageField

from juso.models import TranslationMixin
from juso.events import plugins as event_plugins
from juso.people import plugins as people_plugins
from juso.forms import plugins as form_plugins
from juso.blog import plugins as blog_plugins
from juso.plugins import download
from juso.models import Button
from juso.sections.models import ContentMixin, Section, get_template_list

# Create your models here.


class NameSpace(TranslationMixin):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name} ({self.language_code})"

    class Meta:
        ordering = ['name']
        verbose_name = _("namespace")
        verbose_name_plural = _("namespaces")


class Location(MetaMixin, TranslationMixin):
    regions = [Region(key='images', title=_("images"))]
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField(unique=True)

    street = models.CharField(max_length=200, verbose_name=_("street"))
    city = models.CharField(max_length=100, verbose_name=_("city"))
    zip_code = models.CharField(max_length=20, verbose_name=_("zip code"))
    country = models.CharField(max_length=200, verbose_name=_("country"))

    header_image = ImageField(
        _("header image"), formats={
            'full': ['default', 'darken', ('crop', (1920, 900))],
            'mobile': ['default', ('crop', (740, 600))]
        }, auto_add_fields=True, blank=True, null=True
    )

    section = models.ForeignKey(
        Section, models.SET_NULL, blank=True, null=True,
        verbose_name=_("section")
    )

    website = models.URLField(blank=True, verbose_name=_("website"))

    lng = models.FloatField(verbose_name=_("longitude"), default=0)
    lat = models.FloatField(verbose_name=_("latitude"), default=0)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

    @property
    def address(self):
        return f"{self.street}, {self.zip_code} {self.city}"

    @property
    def image(self):
        if LocationImage.objects.filter(parent=self).exists():
            return LocationImage.objects.filter(parent=self)[0].image
        return self.meta_image

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        ordering = ['name']

    def get_absolute_url(self):
        site = current_site()
        if not self.section or site == self.section.site:
            return reverse_app(
                [f'{site.pk}-events'],
                'location-detail',
                kwargs={
                    'slug': self.slug
                }
            )
        with set_current_site(self.section.site):
            return '//' + self.section.site.host + reverse_app(
                [f'{self.section.site.id}-events'],
                'location-detail',
                urlconf=apps_urlconf(),
                kwargs={
                    'slug': self.slug
                }
            )


LocationPluginBase = create_plugin_base(Location)


class LocationImage(plugins.image.Image, LocationPluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)


class Event(ContentMixin):
    TEMPLATES = get_template_list('events', (
        (
            'default', ('main',),
        ),
    ))

    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))
    slug = models.SlugField(max_length=180)

    location = models.ForeignKey(
        Location, models.SET_NULL,
        blank=True, null=True, verbose_name=_("location")
    )

    namespace = models.ForeignKey(
        NameSpace, models.PROTECT,
        verbose_name=_("namespace")
    )

    @property
    def image(self):
        if Image.objects.filter(parent=self).exists():
            return Image.objects.filter(parent=self)[0].image
        return self.header_image or self.meta_image

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ['start_date']
        indexes = [
            models.Index(fields=[
                'start_date', 'slug', 'section',
            ])
        ]
        constraints = [
            models.UniqueConstraint(fields=[
                'slug', 'start_date', 'section'
            ], name="unique_slugs_for_section_and_date")
        ]

    def get_absolute_url(self):
        site = current_site()
        if site == self.section.site:
            return reverse_app(
                [f'{site.id}-events-{self.namespace}-{self.category}',
                 f'{site.id}-events-{self.namespace}',
                 f'{site.id}-events-{self.category}',
                 f'{site.id}-events'],
                'event-detail',
                kwargs={
                    'slug': self.slug,
                    'day': self.start_date.day,
                    'month': self.start_date.month,
                    'year': self.start_date.year,
                }
            )
        with set_current_site(self.section.site):
            return '//' + self.section.site.host + reverse_app(
                [f'{self.section.site.id}-events-{self.namespace}-{self.category}',
                 f'{self.section.site.id}-events-{self.namespace}',
                 f'{self.section.site.id}-events-{self.category}',
                 f'{self.section.site.id}-events'],
                'event-detail', urlconf=apps_urlconf(),
                kwargs={
                    'slug': self.slug,
                    'day': self.start_date.day,
                    'month': self.start_date.month,
                    'year': self.start_date.year,
                }
            )


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


class Button(Button, PluginBase):
    pass


class ArticlePlugin(blog_plugins.ArticlePlugin, PluginBase):
    pass


class EventPlugin(event_plugins.EventPlugin, PluginBase):
    pass


class FormPlugin(form_plugins.FormPlugin, PluginBase):
    pass


plugins = [
    RichText, Image, HTML, External, Team, Download, Button, ArticlePlugin,
    EventPlugin, FormPlugin,
]
