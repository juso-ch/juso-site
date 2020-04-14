from content_editor.models import Region, Template
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from feincms3.apps import apps_urlconf, reverse_app
from feincms3.mixins import TemplateMixin
from feincms3_meta.models import MetaMixin
from feincms3_sites.middleware import current_site, set_current_site
from feincms3_sites.models import Site
from taggit.managers import TaggableManager
from tree_queries.models import TreeNode

from juso.models import TranslationMixin

# Create your models here.


class Category(TranslationMixin, MetaMixin, TreeNode):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField(verbose_name=_("slug"))

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        site = current_site()
        return reverse_app(
            (str(site.id) + '-categories',),
            'category-detail',
            kwargs={'slug': self.slug}
        )

    def __str__(self):
        return self.name


class Section(TreeNode):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    site = models.OneToOneField(
        Site, models.CASCADE, verbose_name=_("site"),
        related_name="section"
    )
    users = models.ManyToManyField(User, verbose_name=_("users"))
    slug = models.SlugField(unique=True, verbose_name=_("slug"))

    class Meta:
        verbose_name = _("section")
        verbose_name_plural = _("sections")
        ordering = ['name']

    def __str__(self):
        return self.name


class ContentMixin(TranslationMixin, MetaMixin, TemplateMixin):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    slug = models.SlugField(verbose_name=_("slug"))
    author = models.ForeignKey(
        User, models.SET_NULL, null=True, blank=True,
        verbose_name=_("author")
    )

    publication_date = models.DateTimeField(
        default=timezone.now, verbose_name=_("publication date")
    )

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created at")
    )

    edited_date = models.DateTimeField(
        auto_now=True, verbose_name=_("edited at")
    )

    category = models.ForeignKey(
        Category, models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("category")
    )

    tags = TaggableManager(blank=True)

    section = models.ForeignKey(
        Section, models.CASCADE,
        verbose_name=_("section"),
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        unique_together = (('slug', 'section'))
        ordering = ['-publication_date']
        get_latest_by = 'publication_date'


def get_template_list(app_name, templates):
    return [
        Template(
            key=template[0],
            title=_(template[0]).title(),
            template_name=f"{app_name}/{template[0]}.html",
            regions=[
                Region(key=region, title=region.title(), inherited=True)
                for region in template[1]
            ]
        ) for template in templates
    ]
