from django.utils.translation import gettext_lazy as _
from django.db import models

from feincms3.apps import AppsMixin

from content_editor.models import Region, Template, create_plugin_base

from feincms3.mixins import (
    RedirectMixin, MenuMixin,
    LanguageMixin, TemplateMixin
)

from feincms3 import plugins

from feincms3_meta.models import MetaMixin
from feincms3_sites.models import AbstractPage

# Create your models here.


class Page(
    AppsMixin,
    LanguageMixin,
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
        )
    ]
    MENUS = (
        ("main", _("main navigation")),
        ("footer", _("footer navigation")),
    )

    TEMPLATES = [
        Template(
            key="default",
            title=_("default"),
            template_name="pages/default.html",
            regions=(
                Region(key="main", title=_("Main")),
            )
        ),
        Template(
            key="sidebar-right",
            title=_("sidebar right"),
            template_name="pages/sidebar-right.html",
            regions=(
                Region(key="main", title=_("main")),
                Region(key="side", title=_("sidebar"), inherited=True)
            )
        ),
        Template(
            key="sidebar-left",
            title=_("sidebar left"),
            template_name="pages/sidebar-left.html",
            regions=(
                Region(key="main", title=_("main")),
                Region(key="side", title=_("sidebar"), inherited=True)
            )
        ),
        Template(
            key="fullwidth",
            title=_("fullwidth"),
            template_name="pages/fullwidth.html",
            regions=(
                Region(key="main", title=_("main")),
            )
        ),
    ]

    blog_namespace = models.ForeignKey(
        "blog.NameSpace", models.SET_NULL, blank=True, null=True,
        verbose_name=_("namespace")
    )

    category = models.ForeignKey(
        "sections.Category", models.SET_NULL, blank=True, null=True,
        verbose_name=_("category"),
    )


PluginBase = create_plugin_base(Page)


class External(plugins.external.External, PluginBase):
    pass


class RichText(plugins.richtext.RichText, PluginBase):
    pass


class Image(plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)


class HTML(plugins.html.HTML, PluginBase):
    pass
