from content_editor.admin import ContentEditorInline
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from juso.blog.models import Article, NameSpace
from juso.models import TranslationMixin
from juso.sections.models import Category, Section
from juso.utils import number_word


class ArticlePlugin(TranslationMixin):
    articles = models.ManyToManyField(
        Article, related_name='+', related_query_name='+',
        verbose_name=_("articles"), blank=True
    )

    count = models.IntegerField(_("count"), default=3)

    @property
    def columns(self):
        if self.articles.exists():
            return number_word(min(
                self.articles.count(),
                self.count
            ))
        return number_word(self.count)

    namespace = models.ForeignKey(
        NameSpace, models.SET_NULL, related_name='+',
        verbose_name=_("namespace"), blank=True, null=True,
    )

    template_key = models.CharField(
        max_length=100, default='blog/plugins/default.html',
        choices=settings.BLOG_TEMPLATE_CHOICES,
    )

    category = models.ForeignKey(
        Category, models.SET_NULL, related_name='+',
        verbose_name=_("category"), blank=True, null=True,
    )

    sections = models.ManyToManyField(
        Section, related_name='+', related_query_name='+',
        blank=True
    )

    class Meta:
        abstract = True


class ArticlePluginInline(ContentEditorInline):
    autocomplete_fields = [
        'articles', 'category', 'sections',
        'namespace'
    ]

    fieldsets = (
        (None, {
            'fields': (
                'articles',
                'language_code',
                'count',
                'category',
                'namespace',
                'sections',
                'template_key',
                'ordering',
                'region'
            )
        }),
    )


def get_article_list(plugin):
    if plugin.articles.exists():
        return plugin.articles.all()
    articles = Article.objects.filter(
        language_code=plugin.language_code,
    )

    if plugin.category:
        articles = articles.filter(category=plugin.category)

    if plugin.sections.exists():
        articles = articles.filter(section__in=plugin.sections.all())

    return articles[:plugin.count]


def render_articles(plugin, **kwargs):
    return render_to_string(
        plugin.template_key, {
            'articles': get_article_list(plugin),
            'plugin': plugin,
        }
    )
