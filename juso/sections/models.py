import textwrap
from io import BytesIO

from content_editor.models import Region, Template
from django.conf import settings
from django.contrib.auth.models import User
from django.core import files
from django.core.files.storage import get_storage_class
from django.db import models
from django.urls import NoReverseMatch
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from feincms3.apps import reverse_app
from feincms3.mixins import TemplateMixin
from feincms3_meta.models import MetaMixin
from feincms3_sites.middleware import current_site
from feincms3_sites.models import Site
from imagefield.fields import ImageField
from PIL import Image, ImageColor, ImageDraw, ImageFont
from taggit.managers import TaggableManager
from tree_queries.models import TreeNode

from juso.models import TranslationMixin

# Create your models here.


class Category(TranslationMixin, MetaMixin, TreeNode):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField(verbose_name=_("slug"))
    color = models.CharField(max_length=7, verbose_name=_("color"), blank=True,)

    header_image = ImageField(
        _("header image"),
        formats={
            "full": ["default", "darken", ("crop", (1920, 900))],
            "square": ["default", ("crop", (900, 900))],
            "card": ["default", ("crop", (900, 600))],
            "mobile": ["default", ("crop", (740, 600))],
            "some": ["default", ("crop", (1200, 630))],
        },
        auto_add_fields=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        indexes = [models.Index(fields=["slug"])]
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "language_code"], name="unique_slug_for_language"
            )
        ]

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        site = current_site()
        try:
            return reverse_app(
                (str(site.id) + "-categories",),
                "category-detail",
                languages=[self.language_code],
                kwargs={"slug": self.slug},
            )
        except NoReverseMatch:
            return "#"

    def get_header_image(self):
        if self.header_image:
            return self.header_image
        if self.parent:
            return self.parent.get_header_image()
        return None

    def __str__(self):
        return f"{self.name} ({self.language_code})"


class Section(TreeNode):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    site = models.OneToOneField(
        Site, models.CASCADE, verbose_name=_("site"), related_name="section"
    )
    users = models.ManyToManyField(User, verbose_name=_("users"))
    slug = models.SlugField(unique=True, verbose_name=_("slug"))

    class Meta:
        verbose_name = _("section")
        verbose_name_plural = _("sections")
        ordering = ["name"]

    def __str__(self):
        return self.name


class ContentMixin(TranslationMixin, MetaMixin, TemplateMixin):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    slug = models.SlugField(verbose_name=_("slug"), max_length=180)
    author = models.ForeignKey(
        "people.Person",
        models.SET_NULL,
        verbose_name=_("author"),
        blank=True,
        null=True,
    )

    header_image = ImageField(
        _("header image"),
        formats={
            "full": ["default", "darken", ("crop", (1920, 900))],
            "square": ["default", ("crop", (920, 920))],
            "card": ["default", ("crop", (900, 600))],
            "mobile": ["default", ("crop", (740, 600))],
            "some": ["default", ("crop", (1200, 630))],
        },
        auto_add_fields=True,
        blank=True,
        null=True,
    )

    generated_meta_image = models.ImageField(
        _("generated meta image"), upload_to="meta", blank=True, null=True,
    )

    @property
    def image(self):
        try:
            if (
                settings.DEBUG or not self.generated_meta_image
            ) and self.get_header_image():
                orig = self.get_header_image()
                img = Image.open(
                    get_storage_class()().open(
                        self.get_header_image().some[1:].partition("/")[2]
                    )
                )
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(
                    "juso/static/fonts/Montserrat-ExtraBold.ttf", int(1200 / 30)
                )
                color = ImageColor.getcolor(self.get_color(), "RGB")

                title = textwrap.wrap(self.title.upper(), 35, break_long_words=True)
                line = 0
                line_space = 10
                padding_top = 5
                padding_bottom = 14
                padding_side = 15
                line_height = int(1200 / 30) + line_space + padding_bottom + padding_top
                width = 1200
                height = 600

                text_top = height - len(title) * line_height - line_height / 2

                text_color = color
                fill_color = (255, 255, 255)
                border_color = color

                for text in title:
                    line += 1
                    size = font.getsize_multiline(text)
                    x = 30
                    y = text_top + line * line_height
                    draw.rectangle(
                        [
                            x - padding_side,
                            y - padding_top,
                            x + size[0] + padding_side,
                            y + size[1] + padding_bottom,
                        ],
                        fill=fill_color,
                        outline=border_color,
                        width=3,
                    )
                    draw.text(
                        (x, y), text, text_color, font=font,
                    )

                f = BytesIO()

                img.save(f, format="JPEG", quality=100)

                self.generated_meta_image.save(orig.some.split("/")[-1], files.File(f))
            return self.generated_meta_image
        except:  # Anything could happen, but it's not really a priority
            return None

    publication_date = models.DateTimeField(
        default=timezone.now, verbose_name=_("publication date")
    )

    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    edited_date = models.DateTimeField(auto_now=True, verbose_name=_("edited at"))

    category = models.ForeignKey(
        Category, models.SET_NULL, blank=True, null=True, verbose_name=_("category")
    )

    tags = TaggableManager(blank=True)

    section = models.ForeignKey(Section, models.CASCADE, verbose_name=_("section"),)

    def __str__(self):
        return self.title

    def get_header_image(self):
        if self.header_image:
            return self.header_image
        if self.category:
            return self.category.get_header_image()
        return None

    def get_color(self):
        if self.category:
            return self.category.color or settings.DEFAULT_COLOR
        return settings.DEFAULT_COLOR

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=["slug", "section"], name="slug_unique")
        ]
        indexes = [models.Index(fields=["slug"])]
        ordering = ["-publication_date"]
        get_latest_by = "publication_date"

    def meta_images_dict(self):
        if self.meta_image:
            return {
                "image": str(self.meta_image.recommended),
                "image:width": 1200,
                "image:height": 630,
            }
        if self.get_header_image():
            return {
                "image": str(self.get_header_image().some),
                "image:width": 1200,
                "image:height": 630,
            }
        return dict()


def get_template_list(app_name, templates):
    return [
        Template(
            key=template[0],
            title=_(template[0]).title(),
            template_name=f"{app_name}/{template[0]}.html",
            regions=[
                Region(key=region, title=region.title(), inherited=True)
                for region in template[1]
            ],
        )
        for template in templates
    ]
