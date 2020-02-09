from django.db import models
from django.utils.translation import gettext as _

from feincms3.apps import reverse_app

from content_editor.models import create_plugin_base
from feincms3.mixins import LanguageMixin
from feincms3 import plugins

from juso.sections.models import ContentMixin, get_template_list

# Create your models here.


class NameSpace(LanguageMixin):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Article(ContentMixin):
    TEMPLATES = get_template_list('blog', (
        (
            'default', ('main',)
        )
    ))

    namespace = models.ForeignKey(
        NameSpace, models.PROTECT,
        verbose_name=_("namespace")
    )

    def get_absolute_url(self):
        return reverse_app(
            (
                f'{self.section.site_id}-blog-{self.namespace}-{self.category}',
                f'{self.section.site_id}-blog-{self.namespace}',
                f'{self.section.site_id}-blog',
            ),
            'article-detail',
            kwargs={
                'slug': self.slug
            }
        )


PluginBase = create_plugin_base(Article)


class External(plugins.external.External, PluginBase):
    pass


class RichText(plugins.richtext.RichText, PluginBase):
    pass


class Image(plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)


class HTML(plugins.html.HTML, PluginBase):
    pass
