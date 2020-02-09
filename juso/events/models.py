from django.db import models
from django.utils.translation import gettext as _

from content_editor.models import create_plugin_base
from feincms3.mixins import LanguageMixin

from feincms3 import plugins
from juso.sections.models import ContentMixin, get_template_list

# Create your models here.


class NameSpace(LanguageMixin):
    name = models.CharField(max_length=200)
    slug = models.SlugField()


class Event(ContentMixin):
    TEMPLATES = get_template_list('events', (
        (
            'default', ('main',)
        )
    ))

    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))

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
