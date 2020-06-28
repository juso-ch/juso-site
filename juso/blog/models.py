from content_editor.models import create_plugin_base
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import NoReverseMatch
from feincms3 import plugins
from feincms3.apps import apps_urlconf, reverse_app
from feincms3_sites.middleware import current_site, set_current_site
import json
import bleach

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
        return f"{self.name} ({self.language_code})"

    class Meta:
        verbose_name = _("name space")
        verbose_name_plural = _("name spaces")
        ordering = ["slug"]


class Article(ContentMixin):
    TEMPLATES = get_template_list(
        "blog",
        (
            ("default", ("main",)),
            ("sidebar-right", ("main", "sidebar")),
            ("sidebar-left", ("main", "sidebar")),
            ("fullwidth", ("main",)),
        ),
    )

    namespace = models.ForeignKey(
        NameSpace, models.PROTECT, verbose_name=_("namespace")
    )

    @property
    def tagline(self):
        if RichText.objects.filter(parent=self).exists():
            return bleach.clean(
                RichText.objects.filter(parent=self)[0].text, strip=True, tags=[],
            )
        if self.meta_description:
            return self.meta_description
        return ""

    def get_absolute_url(self):
        try:
            site = current_site()
            if site == self.section.site:
                return reverse_app(
                    (
                        f"{site.id}-blog-{self.namespace.name}-{self.category}",
                        f"{site.id}-blog-{self.namespace.name}",
                        f"{site.id}-blog-{self.category}",
                        f"{site.id}-blog",
                    ),
                    "article-detail",
                    kwargs={"slug": self.slug},
                    languages=[self.language_code],
                )
            with set_current_site(self.section.site):
                site = self.section.site
                return (
                    "//"
                    + self.section.site.host
                    + reverse_app(
                        [
                            f'{site.id}-blog-{self.namespace.name}-{self.category or ""}',
                            f"{site.id}-blog-{self.namespace.name}",
                            f'{site.id}-blog-{self.category or ""}',
                            f"{site.id}-blog",
                        ],
                        "article-detail",
                        urlconf=apps_urlconf(),
                        kwargs={"slug": self.slug},
                        languages=[self.language_code],
                    )
                )
        except NoReverseMatch:
            return "#"

    def webpush_data(self, page):
        if favicon := page.top_page().favicon:
            icon = f"https://{page.site.host}" + favicon["512"]
        else:
            icon = "https://" + page.site.host + "/static/logo.png"
        return json.dumps(
            {
                "title": self.title,
                "tagline": self.tagline[:280],
                "icon": icon,
                "url": self.get_full_url(),
                "badge": "https://" + page.site.host + "/static/badge.png",
                "publication_date": self.publication_date.isoformat(),
                "image": ("https://" + page.site.host + self.get_header_image().full)
                if self.get_header_image()
                else "",
            }
        )

    def get_full_url(self):
        url = self.get_absolute_url()
        if url.startswith("//"):
            return "https:" + url
        else:
            return "https://" + self.section.site.host + url

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")
        ordering = ["-publication_date"]


class WPImport(models.Model):
    slug = models.SlugField(_("slug"), unique=True)
    import_file = models.FileField(verbose_name=_("wordpress file"))
    section = models.ForeignKey(
        "sections.Section", models.CASCADE, verbose_name=_("section")
    )
    default_namespace = models.ForeignKey(
        NameSpace, models.CASCADE, related_name="+", verbose_name=_("default namespace")
    )
    completed = models.BooleanField(default=False, verbose_name=_("completed"))

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = _("wordpress import")
        verbose_name_plural = _("wordpress imports")


class NamespaceMapping(models.Model):
    wp_import = models.ForeignKey(WPImport, models.CASCADE, related_name="mappings")
    nicename = models.CharField(_("name"), max_length=100)
    target = models.ForeignKey(NameSpace, models.CASCADE, related_name="+")

    def __str__(self):
        return self.nicename


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
    fullwidth = models.BooleanField(_("full width"), default=False)

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
    RichText,
    Image,
    HTML,
    External,
    Team,
    Download,
    Button,
    EventPlugin,
    GlossaryRichText,
    FormPlugin,
    ArticlePlugin,
]
