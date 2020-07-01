from content_editor.admin import ContentEditorInline
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from juso.models import TranslationMixin
from juso.sections.models import Category, Section
from juso.utils import number_word


class ArticlePlugin(TranslationMixin):
    articles = models.ManyToManyField(
        "blog.Article",
        related_name="%(app_label)s_%(class)s",
        verbose_name=_("articles"),
        blank=True,
    )

    title = models.CharField(_("title"), blank=True, max_length=180)

    count = models.IntegerField(_("count"), default=3)

    @property
    def columns(self):
        if self.articles.exists():
            return number_word(min(self.articles.count(), self.count))
        return number_word(self.count)

    namespace = models.ForeignKey(
        "blog.NameSpace",
        models.SET_NULL,
        related_name="+",
        verbose_name=_("namespace"),
        blank=True,
        null=True,
    )

    template_key = models.CharField(
        max_length=100,
        default="blog/plugins/default.html",
        choices=settings.BLOG_TEMPLATE_CHOICES,
    )

    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        related_name="+",
        verbose_name=_("category"),
        blank=True,
        null=True,
    )

    sections = models.ManyToManyField(
        Section, related_name="%(app_label)s_%(class)s", blank=True
    )

    all_articles = models.ForeignKey(
        "pages.Page",
        models.CASCADE,
        related_name="+",
        blank=True,
        verbose_name=_("page with all articles"),
        null=True,
    )

    all_articles_override = models.CharField(
        _("all article link text"), max_length=180, blank=True,
    )

    structured_data = models.BooleanField(_("include structured data"), default=False)

    class Meta:
        abstract = True
        verbose_name = _("article plugin")
        verbose_name_plural = _("article plugins")

    def __str__(self):
        return self.title or gettext("articles")


class ArticlePluginInline(ContentEditorInline):
    autocomplete_fields = [
        "articles",
        "category",
        "sections",
        "namespace",
        "all_articles",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "count",
                    "category",
                    "namespace",
                    "ordering",
                    "region",
                )
            },
        ),
        (
            _("advanced"),
            {
                "classes": ("collapse",),
                "fields": (
                    "articles",
                    "sections",
                    "language_code",
                    "template_key",
                    "structured_data",
                    "all_articles",
                    "all_articles_override",
                ),
            },
        ),
    )


def get_article_list(plugin):
    if plugin.articles.exists():
        return plugin.articles.all()
    from juso.blog.models import Article

    articles = Article.objects.filter(language_code=plugin.language_code,)

    if plugin.category:
        articles = articles.filter(category=plugin.category)

    if plugin.sections.exists():
        articles = articles.filter(section__in=plugin.sections.all())
    else:
        articles = articles.filter(section=plugin.parent.site.section)

    if plugin.namespace:
        articles = articles.filter(namespace=plugin.namespace)

    return articles[: plugin.count]


def render_articles(plugin, **kwargs):
    return render_to_string(
        plugin.template_key,
        {"article_list": get_article_list(plugin), "plugin": plugin,},
    )
