from content_editor.models import create_plugin_base
from django.db import models
from django.utils.translation import gettext as _
from feincms3 import plugins
from feincms3.apps import reverse_app
from feincms3_sites.middleware import current_site, set_current_site

from juso.models import TranslationMixin
from juso.plugins import download
from juso.sections.models import ContentMixin, get_template_list

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
            'sidebar-right', ('main', 'side')
        ),
        (
            'sidebar-left', ('main', 'side')
        ),
        (
            'fullwidth', ('main',)
        )
    ))

    namespace = models.ForeignKey(
        NameSpace, models.PROTECT,
        verbose_name=_("namespace")
    )

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
                (f'{site.id}-blog-{self.namespace}-{self.category}',
                 f'{site.id}-blog-{self.namespace}',
                 f'{site.id}-blog-{self.category}',
                 f'{site.id}-blog',),
                'article-detail',
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


class Image(plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)


class HTML(plugins.html.HTML, PluginBase):
    pass


class Download(download.Download, PluginBase):
    pass


plugins = [RichText, Image, HTML, External, Download]
