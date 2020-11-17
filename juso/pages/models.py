from content_editor.models import create_plugin_base
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from feincms3 import plugins as feincms3_plugins
from feincms3.apps import AppsMixin
from feincms3.mixins import MenuMixin, RedirectMixin, TemplateMixin
from feincms3_meta.models import MetaMixin
from feincms3_sites.middleware import current_site
from feincms3_sites.models import AbstractPage
from imagefield.fields import ImageField
from imagefield.processing import register
from PIL import ImageEnhance, ImageOps
import bleach

from juso import models as juso
from juso.blog import plugins as article_plugins
from juso.events import plugins as event_plugins
from juso.forms import plugins as form_plugins
from juso.glossary.models import GlossaryContent
from juso.models import TranslationMixin
from juso.people import plugins as people_plugins
from juso.plugins import download
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
                "app_instance_namespace": lambda page: "-".join(
                    (
                        str(x)
                        for x in [
                            page.site_id,
                            page.application,
                            page.blog_namespace.name if page.blog_namespace else None,
                            page.category,
                        ]
                        if x
                    )
                ),
            },
        ),
        (
            "people",
            _("people"),
            {
                "urlconf": "juso.people.urls",
                "app_instance_namespace": lambda page: "-".join(
                    (
                        str(x)
                        for x in [
                            page.site_id,
                            page.application,
                        ]
                        if x
                    )
                ),
            },
        ),
        (
            "events",
            _("events"),
            {
                "urlconf": "juso.events.urls",
                "app_instance_namespace": lambda page: "-".join(
                    (
                        str(x)
                        for x in [
                            page.site_id,
                            page.application,
                            page.category,
                        ]
                        if x
                    )
                ),
            },
        ),
        (
            "categories",
            _("categories"),
            {
                "urlconf": "juso.sections.urls",
                "app_instance_namespace": lambda page: str(page.site_id)
                + "-"
                + "categories",
            },
        ),
        (
            "glossary",
            _("glossary"),
            {
                "urlconf": "juso.glossary.urls",
                "app_instance_namespace": lambda page: str(page.site_id)
                + "-"
                + "glossary",
            },
        ),
        (
            "collection",
            _("collection"),
            {
                "urlconf": "juso.link_collections.urls",
                "required_fields": ["collection"],
                "app_instance_namespace": lambda page: str(page.slug) + "-collections",
            },
        ),
    ]

    MENUS = (
        ("main", _("main navigation")),
        ("top", _("top navigation")),
        ("buttons", _("button navigation")),
        ("footer", _("footer navigation")),
        ("quicklink", _("quickinks")),
    )

    TEMPLATES = get_template_list(
        "pages",
        (
            ("default", ("main", "footer")),
            ("feature_top", ("main", "sidebar", "feature")),
        ),
    )

    is_landing_page = models.BooleanField(
        default=False,
        verbose_name=_("is landing page"),
    )

    position = models.PositiveIntegerField(
        db_index=True,
        default=10,
        validators=[
            MinValueValidator(
                limit_value=1,
                message=_("Position is expected to be greater than zero."),
            )
        ],
    )

    blog_namespace = models.ForeignKey(
        "blog.NameSpace",
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("namespace (blog)"),
    )

    sections = models.ManyToManyField(
        "sections.Section",
        verbose_name=_("sections"),
        blank=True,
    )

    category = models.ForeignKey(
        "sections.Category",
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("category"),
    )

    collection = models.ForeignKey(
        "link_collections.Collection",
        models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("collection"),
    )

    header_image = ImageField(
        _("header image"),
        formats={
            "full": ["default", "darken", ("crop", (1920, 900))],
            "square": ["default", ("crop", (960, 960))],
            "card": ["default", ("crop", (900, 600))],
            "mobile": ["default", ("crop", (740, 600))],
        },
        auto_add_fields=True,
        blank=True,
        null=True,
    )

    featured_categories = models.ManyToManyField(
        "sections.Category",
        blank=True,
        verbose_name=_("featured categories"),
        related_name="featured",
    )

    in_meta = models.BooleanField(_("in meta menu"), default=False)

    is_navigation = models.BooleanField(_("display navigation"), default=False)

    lastmod = models.DateTimeField(_("lastmod"), auto_now=True)

    logo = models.TextField(_("logo"), blank=True)

    google_site_verification = models.CharField(max_length=60, blank=True)

    favicon = ImageField(
        _("favicon"),
        formats={
            "192": ["default", ("crop", (192, 192))],
            "512": ["default", ("crop", (512, 512))],
            "180": ["default", ("crop", (180, 180))],
            "128": ["default", ("crop", (128, 128))],
            "32": ["default", ("crop", (32, 32))],
            "16": ["default", ("crop", (16, 16))],
        },
        blank=True,
        auto_add_fields=True,
    )

    primary_color = models.CharField(_("primary color"), max_length=7, blank=True)

    css_vars = models.TextField(_("css vars"), blank=True)
    fonts = models.TextField(
        _("fonts"), default="klima", help_text=_("fonts loaded on the site")
    )

    @property
    def description(self):
        return self.meta_description or self.tagline[:300]

    @property
    def tagline(self):
        if RichText.objects.filter(parent=self).exists():
            return bleach.clean(
                RichText.objects.filter(parent=self)[0].text,
                strip=True,
                tags=[],
            )
        if self.meta_description:
            return self.meta_description
        return ""

    def get_fonts(self):
        for font in self.fonts.split("\n"):
            yield font.strip() + ".css"

    prefetches = models.TextField(
        _("prefetch"),
        default="""fonts/klima-regular-web.woff2:font
fonts/klima-regular-italic-web.woff2:font
fonts/klima-bold-web.woff2:font
fonts/klima-bold-italic-web.woff2:font""",
        help_text=_("files that should be preloaded"),
    )

    def get_prefeteches(self):
        for prefetch in self.prefetches.split("\n"):
            yield prefetch.strip().split(":")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_landing_page = self.is_landing_page

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.is_landing_page or self._is_landing_page == self.is_landing_page:
            return super().save(*args, **kwargs)
        Page.objects.filter(
            is_landing_page=True,
            language_code=self.language_code,
            site=self.site,
        ).update(is_landing_page=False)
        return super().save(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):

        if self.redirect_to_url or self.redirect_to_page:
            return self.redirect_to_url or self.redirect_to_page.get_absolute_url()

        site = current_site()
        if site == self.site:
            return super().get_absolute_url(*args, **kwargs)
        return "//" + self.site.host + super().get_absolute_url()

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
        return header_image

    def top_page(self):
        return self.ancestors(include_self=True)[0]

    def get_translation_for(self, language_code):
        r = super().get_translation_for(language_code)
        if r:
            return r
        if self.parent:
            return self.parent.get_translation_for(language_code)
        return None

    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("pages")
        indexes = [
            models.Index(
                fields=[
                    "path",
                    "site_id",
                    "language_code",
                    "is_active",
                ]
            ),
            models.Index(
                fields=[
                    "is_landing_page",
                    "site_id",
                    "language_code",
                ]
            ),
            models.Index(fields=["is_active", "menu", "language_code"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["path", "site_id"], name="unique_page_for_path"
            )
        ]


class PagesPlugin(models.Model):
    pages = models.ManyToManyField(Page, related_name="+")

    class Meta:
        abstract = True


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


class FormEntryCounterPlugin(form_plugins.EntryCounter, PluginBase):
    pass


class CandidaturePlugin(people_plugins.CandidatePlugin, PluginBase):
    pass


class CategoryLinking(models.Model):
    page = models.ForeignKey(Page, models.CASCADE)
    category = models.ForeignKey("sections.Category", models.CASCADE)

    description = feincms3_plugins.richtext.CleansedRichTextField(blank=True)
    order = models.IntegerField(default=10)
    other_site = models.ForeignKey(
        Page, models.CASCADE, blank=True, null=True, related_name="+"
    )

    def __str__(self):
        return self.category.name

    def get_absolute_url(self):
        return self.page.get_absolute_url() + self.category.slug + "/"

    class Meta:
        ordering = ["order"]


class NavigationPlugin(PagesPlugin, PluginBase):
    pass


class VotingRecommendationPlugin(juso.VotingRecommendation, PluginBase):
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
    ArticlePlugin,
    FormPlugin,
    GlossaryRichText,
    FormEntryCounterPlugin,
    NavigationPlugin,
    CandidaturePlugin,
    VotingRecommendationPlugin,
]
