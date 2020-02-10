from content_editor.models import create_plugin_base
from django.db import models
from django.utils.translation import gettext as _
from feincms3 import plugins
from feincms3.mixins import LanguageMixin
from feincms3_meta.models import MetaMixin
from taggit.managers import TaggableManager

from juso.sections.models import ContentMixin, get_template_list

# Create your models here.


class NameSpace(LanguageMixin):
    name = models.CharField(max_length=200)
    slug = models.SlugField()


class Location(MetaMixin):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=200)

    website = models.URLField(blank=True)

    lng = models.FloatField()
    lat = models.FloatField()

    tags = TaggableManager()


class Event(ContentMixin):
    TEMPLATES = get_template_list('events', (
        (
            'default', ('main',)
        )
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


PluginBase = create_plugin_base(Event)


class External(plugins.external.External, PluginBase):
    pass


class RichText(plugins.richtext.RichText, PluginBase):
    pass


class Image(plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)


class HTML(plugins.html.HTML, PluginBase):
    pass
