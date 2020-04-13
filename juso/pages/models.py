from content_editor.models import create_plugin_base
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from feincms3 import plugins
from feincms3.apps import AppsMixin
from feincms3.mixins import MenuMixin, RedirectMixin, TemplateMixin
from feincms3_meta.models import MetaMixin
from feincms3_sites.middleware import current_site, set_current_site
from feincms3_sites.models import AbstractPage

from fomantic_ui import models as fomantic
from juso.models import TranslationMixin
from juso.people import plugins as people_plugins
from juso.events import plugins as event_plugins
from juso.blog import plugins as article_plugins
from juso.plugins import download
from juso.sections.models import get_template_list
from juso.forms import plugins as form_plugins

# Create your models here.


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
                        page.blog_namespace,
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
                        page.event_namespace,
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
                "app_instance_namespace": lambda page: (
                    str(page.site_id) + '-' + 'categories'
                )
            },
        ),
    ]

    MENUS = (
        ("main", _("main navigation")),
        ("footer", _("footer navigation")),
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

    featured_categories = models.ManyToManyField(
        "sections.Category", blank=True, verbose_name=_("featured categories"),
        related_name="featured"
    )

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.is_landing_page:
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

    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("page")


PluginBase = create_plugin_base(Page)


class External(plugins.external.External, PluginBase):
    class Meta:
        verbose_name = _("external")
        verbose_name = _("external")


class RichText(plugins.richtext.RichText, PluginBase):
    class Meta:
        verbose_name = _("rich text")
        verbose_name = _("rich text")


class Image(plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)
    title = models.CharField(_("title"), max_length=200, blank=True)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")


class Download(download.Download, PluginBase):
    pass


class HTML(plugins.html.HTML, PluginBase):
    class Meta:
        verbose_name = _("HTML")
        verbose_name_plural = _("HTML")


class Team(people_plugins.TeamPlugin, PluginBase):
    pass


class Button(fomantic.Button, PluginBase):
    pass


class Divider(fomantic.Divider, PluginBase):
    pass


class Header(fomantic.Header, PluginBase):
    pass


class EventPlugin(event_plugins.EventPlugin, PluginBase):
    pass


class ArticlePlugin(article_plugins.ArticlePlugin, PluginBase):
    pass


class FormPlugin(form_plugins.FormPlugin, PluginBase):
    pass


plugins = [
    RichText, Image, HTML, External, Team, Download, Button, Divider, Header,
    EventPlugin, ArticlePlugin, FormPlugin
]
