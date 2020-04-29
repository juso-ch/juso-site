from content_editor.models import create_plugin_base
from django.db import models
from django.utils.translation import gettext as _
from feincms3 import plugins
from feincms3.apps import apps_urlconf, reverse_app
from feincms3_sites.middleware import current_site, set_current_site

from imagefield.fields import ImageField

from juso import models as juso
from juso.events import plugins as event_plugins
from juso.forms import plugins as form_plugins
from juso.models import TranslationMixin
from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.sections.models import ContentMixin, get_template_list
from juso.glossary.models import GlossaryContent
from .plugins import ArticlePlugin

# Create your models here.


class NameSpace(TranslationMixin):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("name space")
        verbose_name_plural = _("name spaces")
        ordering = ['slug']


class Article(ContentMixin):
    TEMPLATES = get_template_list('blog', (
        (
            'default', ('main',)
        ),
        (
            'sidebar-right', ('main', 'sidebar')
        ),
        (
            'sidebar-left', ('main', 'sidebar')
        ),
        (
            'fullwidth', ('main',)
        )
    ))

    namespace = models.ForeignKey(
        NameSpace, models.PROTECT,
        verbose_name=_("namespace")
    )

    @property
    def image(self):
        if Image.objects.filter(parent=self).exists():
            return Image.objects.filter(parent=self)[0].image
        return self.meta_image

    def get_absolute_url(self):
        site = current_site()
        if site == self.section.site:
            return reverse_app(
                (f'{site.id}-blog-{self.namespace}-{self.category}',
                 f'{site.id}-blog-{self.namespace}',
                 f'{site.id}-blog-{self.category}',
                 f'{site.id}-blog',),
                'article-detail',
                kwargs={
                    'slug': self.slug
                }
            )
        with set_current_site(self.section.site):
            site = self.section.site
            return '//' + self.section.site.host + reverse_app(
                [f'{site.id}-blog-{self.namespace}-{self.category or ""}',
                 f'{site.id}-blog-{self.namespace}',
                 f'{site.id}-blog-{self.category or ""}',
                 f'{site.id}-blog'],
                'article-detail',
                urlconf=apps_urlconf(),
                kwargs={
                    'slug': self.slug
                }
            )

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")
        ordering = ['-publication_date']


PluginBase = create_plugin_base(Article)


class External(plugins.external.External, PluginBase):
    pass


class RichText(plugins.richtext.RichText, PluginBase):
    pass


class GlossaryRichText(GlossaryContent, PluginBase):
    class Meta:
        verbose_name = _("glossary text")


class Image(plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)
    title = models.CharField(_("title"), max_length=200, blank=True)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")


class HTML(plugins.html.HTML, PluginBase):
    pass


class Download(download.Download, PluginBase):
    pass


class Button(juso.Button, PluginBase):
    pass


class Team(people_plugins.TeamPlugin, PluginBase):
    pass


class EventPlugin(event_plugins.EventPlugin, PluginBase):
    pass


class ArticlePlugin(ArticlePlugin, PluginBase):
    pass


class FormPlugin(form_plugins.FormPlugin, PluginBase):
    pass


plugins = [
    RichText, Image, HTML, External, Team, Download, Button,
    EventPlugin, GlossaryContent, FormPlugin, ArticlePlugin
]
