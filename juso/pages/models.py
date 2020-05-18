from content_editor.models import create_plugin_base
from django.db import models, transaction
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from feincms3 import plugins as feincms3_plugins
from feincms3.apps import AppsMixin
from feincms3.mixins import MenuMixin, RedirectMixin, TemplateMixin
from feincms3_meta.models import MetaMixin
from feincms3_sites.middleware import current_site, set_current_site
from feincms3_sites.models import AbstractPage

from imagefield.fields import ImageField

from PIL import ImageOps, ImageEnhance
from imagefield.processing import register

from juso import models as juso
from juso.blog import plugins as article_plugins
from juso.events import plugins as event_plugins
from juso.forms import plugins as form_plugins
from juso.models import TranslationMixin
from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.glossary.models import GlossaryContent
from juso.sections.models import get_template_list

# Create your models here.


@register
def grayscale(get_image):
    def processor(image, context):
        image = get_image(image, context)
        return ImageOps.grayscale(image)
    return processor


@register
def darken(get_image):
    def processor(image, context):
        image = get_image(image, context)
        return ImageEnhance.Brightness(image).enhance(0.5)
    return processor


class Page(
    AppsMixin,
    TranslationMixin,
    MetaMixin,
    TemplateMixin,
    RedirectMixin,
    MenuMixin,
    AbstractPage,
):
    APPLICATIONS = [
        (
            "blog",
            _("blog"),
            {
                "urlconf": "juso.blog.urls",
                "app_instance_namespace": lambda page: '-'.join(
                    (str(x) for x in [
                        page.site_id,
                        page.application,
                        page.blog_namespace.name,
                        page.category
                    ] if x))
            }
        ),
        (
            'people',
            _("people"),
            {
                "urlconf": "juso.people.urls",
                "app_instance_namespace": lambda page: '-'.join(
                    (str(x) for x in [
                        page.site_id,
                        page.application,
                    ] if x)
                )
            }
        ),
        (
            'events',
            _("events"),
            {
                "urlconf": "juso.events.urls",
                "app_instance_namespace": lambda page: '-'.join(
                    (str(x) for x in [
                        page.site_id,
                        page.application,
                        page.category,
                    ] if x)
                )
            },
        ),
        (
            'categories',
            _('categories'),
            {
                "urlconf": "juso.sections.urls",
                'app_instance_namespace': lambda page: str(page.site_id) + '-' + 'categories'
            },
        ),
        (
            'glossary',
            _("glossary"),
            {
                'urlconf': "juso.glossary.urls",
                'app_instance_namespace': lambda page: str(page.site_id) + '-' + 'glossary'
            }
        ),
        (
            'collection',
            _("collection"),
            {
                'urlconf': "juso.link_collections.urls",
                "required_fields": ['collection'],
                'app_instance_namespace': lambda page: str(page.slug) + '-collections'
            }
        )
    ]

    MENUS = (
        ("main", _("main navigation")),
        ("top", _("top navigation")),
        ("buttons", _("button navigation")),
        ("footer", _("footer navigation")),
        ("quicklink", _("quickinks")),
    )

    TEMPLATES = get_template_list('pages', (
        (
            'default', ('main', 'footer')
        ),
        (
            'sidebar-right', ('main', 'sidebar', 'footer')
        ),
        (
            'sidebar-left', ('main', 'sidebar', 'footer')
        ),
        (
            'sidebar-both', ('main', 'left', 'right', 'footer')
        ),
        (
            'fullwidth', ('main', 'footer')
        )
    ))

    is_landing_page = models.BooleanField(
        default=False,
        verbose_name=_("is landing page"),
    )

    blog_namespace = models.ForeignKey(
        "blog.NameSpace", models.SET_NULL, blank=True, null=True,
        verbose_name=_("namespace (blog)")
    )

    event_namespace = models.ForeignKey(
        "events.NameSpace", models.SET_NULL, blank=True, null=True,
        verbose_name=_("namespace (event)")
    )

    sections = models.ManyToManyField(
        "sections.Section", verbose_name=_("sections"), blank=True,
    )

    category = models.ForeignKey(
        "sections.Category", models.SET_NULL, blank=True, null=True,
        verbose_name=_("category"),
    )

    collection = models.ForeignKey(
        "link_collections.Collection", models.CASCADE, blank=True,
        null=True, verbose_name=_("collection")
    )

    header_image = ImageField(
        _("header image"), formats={
            'full': ['default', 'darken', ('crop', (1920, 900))],
            'square': ['default', ('crop', (960, 960))],
            'mobile': ['default', ('crop', (740, 600))],
        }, auto_add_fields=True, blank=True, null=True
    )

    featured_categories = models.ManyToManyField(
        "sections.Category", blank=True, verbose_name=_("featured categories"),
        related_name="featured"
    )

    in_meta = models.BooleanField(_("in meta menu"), default=False)

    is_navigation = models.BooleanField(_("display navigation"), default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_landing_page = self.is_landing_page

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.is_landing_page or\
           self._is_landing_page == self.is_landing_page:
            return super().save(*args, **kwargs)
        Page.objects.filter(
            is_landing_page=True,
            language_code=self.language_code,
            site=self.site,
        ).update(is_landing_page=False)
        return super().save(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):
        site = current_site()
        if site == self.site:
            return super().get_absolute_url(*args, **kwargs)
        return '//' + self.site.host + super().get_absolute_url()

    def get_category_color(self):
        return self.category.color if self.category else settings.DEFAULT_COLOR

    def get_header_image(self):
        header_image = None
        if self.header_image:
            header_image = self.header_image
        if self.parent:
            header_image = header_image or self.parent.get_header_image()
        if self.category:
            header_image = header_image or self.category.get_header_image()
        print(header_image)
        return header_image

    def get_translation_for(self, language_code):
        r = super().get_translation_for(language_code)
        if r:
            return r
        if self.parent:
            return self.parent.get_translation_for(language_code)
        return None

    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("page")
        #ordering = ['parent_id', 'position']


PluginBase = create_plugin_base(Page)


class External(feincms3_plugins.external.External, PluginBase):
    class Meta:
        verbose_name = _("external")


class RichText(feincms3_plugins.richtext.RichText, PluginBase):
    class Meta:
        verbose_name = _("rich text")


class GlossaryRichText(GlossaryContent, PluginBase):
    class Meta:
        verbose_name = _("glossary text")


class Image(feincms3_plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)
    title = models.CharField(_("title"), max_length=200, blank=True)
    fullwidth = models.BooleanField(_("full width"), default=False)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")


class Download(download.Download, PluginBase):
    pass


class HTML(feincms3_plugins.html.HTML, PluginBase):
    class Meta:
        verbose_name = _("HTML")
        verbose_name_plural = _("HTML")


class Team(people_plugins.TeamPlugin, PluginBase):
    pass


class Button(juso.Button, PluginBase):
    pass


class EventPlugin(event_plugins.EventPlugin, PluginBase):
    pass


class ArticlePlugin(article_plugins.ArticlePlugin, PluginBase):
    pass


class FormPlugin(form_plugins.FormPlugin, PluginBase):
    pass


class CategoryLinking(models.Model):
    page = models.ForeignKey(Page, models.CASCADE)
    category = models.ForeignKey("sections.Category", models.CASCADE)

    description = feincms3_plugins.richtext.CleansedRichTextField()
    order = models.IntegerField(default=10)

    def __str__(self):
        return self.category.name

    class Meta:
        ordering = ['order']


plugins = [
    RichText, Image, HTML, External, Team, Download, Button,
    EventPlugin, ArticlePlugin, FormPlugin, GlossaryRichText,
]
