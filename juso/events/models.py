from content_editor.models import create_plugin_base, Region
from django.db import models
from django.utils.translation import gettext as _
from feincms3 import plugins
from feincms3.mixins import LanguageMixin
from feincms3_meta.models import MetaMixin
from taggit.managers import TaggableManager
from feincms3.apps import reverse_app

from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.sections.models import ContentMixin, get_template_list, Section

# Create your models here.


class NameSpace(LanguageMixin):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Location(MetaMixin):
    regions = [Region(key='images', title=_("images"))]
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField(unique=True)

    street = models.CharField(max_length=200, verbose_name=_("street"))
    city = models.CharField(max_length=100, verbose_name=_("city"))
    zip_code = models.CharField(max_length=20, verbose_name=_("zip code"))
    country = models.CharField(max_length=200, verbose_name=_("country"))

    section = models.ForeignKey(
        Section, models.SET_NULL, blank=True, null=True,
        verbose_name=_("section")
    )

    website = models.URLField(blank=True, verbose_name=_("website"))

    lng = models.FloatField(verbose_name=_("longitude"))
    lat = models.FloatField(verbose_name=_("latitude"))

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        ordering = ['name']

    def get_absolute_url(self):
        if not self.section:
            return reverse_app(
                [f'1-events'],
                'location-detail',
                kwargs={
                    'slug': self.slug
                }
            )
        return reverse_app(
            [f'{self.section.site_id}-events'],
            'location-detail',
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

    location = models.ForeignKey(
        Location, models.SET_NULL,
        blank=True, null=True, verbose_name=_("location")
    )

    namespace = models.ForeignKey(
        NameSpace, models.PROTECT,
        verbose_name=_("namespace")
    )

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ['-start_date']

    def get_absolute_url(self):
        return reverse_app(
            [f'{self.section.site_id}-events-{self.namespace}-{self.category}',
             f'{self.section.site_id}-events-{self.namespace}',
             f'{self.section.site_id}-events-{self.category}',
             f'{self.section.site_id}-events'],
            'event-detail',
            kwargs={
                'slug': self.slug
            }
        )


PluginBase = create_plugin_base(Event)


class External(plugins.external.External, PluginBase):
    pass


class RichText(plugins.richtext.RichText, PluginBase):
    pass


class Image(plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)


class HTML(plugins.html.HTML, PluginBase):
    pass


class Download(download.Download, PluginBase):
    pass


class Team(people_plugins.TeamPlugin, PluginBase):
    pass


plugins = [External, RichText, Image, HTML, Download, Team]
