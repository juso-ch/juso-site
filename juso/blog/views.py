from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, SearchHeadline
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.syndication.views import Feed
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from feincms3.apps import page_for_app_request
from feincms3.regions import Regions
from feincms3.shortcuts import render_list
from feincms3_meta.utils import meta_tags

from juso import pages
from juso.blog import models
from juso.blog.renderer import renderer
from juso.search import consume
from juso.sections.models import Category

# Create your views here.


def articles_for_page(page, qs=None, allow_future=False):
    qs = qs if qs else models.Article.objects.filter(language_code=page.language_code)

    if page.category:
        qs = qs.filter(category=page.category)

    if page.blog_namespace:
        qs = qs.filter(namespace=page.blog_namespace)

    if page.sections.count():
        qs = qs.filter(section__in=page.sections.all())
    elif hasattr(page.site, "section"):
        qs = qs.filter(section=page.site.section)

    if allow_future:
        return qs
    else:
        return qs.filter(publication_date__lte=timezone.now())


@ensure_csrf_cookie
def article_list(request):
    page = page_for_app_request(request)
    page.activate_language(request)

    article_list = articles_for_page(page)
    category_list = Category.objects.filter(article__in=article_list).distinct()

    if request.GET.get("category", None):
        article_list = article_list.filter(
            category__slug__in=request.GET.getlist("category")
        )

    q = ""

    if request.GET.get("search", ""):
        vector = (
            SearchVector("title", weight="A")
            + SearchVector("category__name", weight="A")
            + SearchVector("blog_richtext_set__text", weight="A")
            + SearchVector("blog_glossaryrichtext_set__text", weight="A")
            + SearchVector("author__first_name", weight="B")
            + SearchVector("author__last_name", weight="B")
        )
        query = consume(request.GET["search"])
        q = request.GET["search"]
        article_list = (
            article_list.annotate(
                rank=SearchRank(vector, query, cover_density=True),
                headline=SearchHeadline(
                    'blog_richtext_set__text',
                    query,
                    max_words=25,
                    min_words=20,
                    max_fragments=2,
                )
            )
            .filter(rank__gt=0)
            .order_by("-rank")
            .distinct()
        )

    ancestors = list(page.ancestors().reverse())
    return render_list(
        request,
        article_list,
        {
            "page": page,
            "q": q,
            "header_image": page.get_header_image(),
            "vapid_public_key": settings.VAPID_PUBLIC_KEY,
            "category_list": category_list,
            "meta_tags": meta_tags([page] + ancestors, request=request),
            "regions": Regions.from_item(
                page, renderer=pages.renderer.renderer, timeout=60,
            ),
        },
        paginate_by=12,
    )


@ensure_csrf_cookie
def category_list(request, slug):
    page = page_for_app_request(request)
    page.activate_language(request)

    articles = articles_for_page(page).filter(category__slug=slug)

    ancestors = list(page.ancestors().reverse())

    return render_list(
        request,
        articles,
        {
            "page": page,
            "header_image": page.get_header_image(),
            "meta_tags": meta_tags([page] + ancestors, request=request),
            "regions": Regions.from_item(
                page,
                renderer=pages.renderer.renderer,
                timeout=60,
                inherit_from=ancestors,
            ),
        },
        paginate_by=10,
    )


@ensure_csrf_cookie
def article_detail(request, slug):
    page = page_for_app_request(request)
    page.activate_language(request)

    article = get_object_or_404(articles_for_page(page, allow_future=True), slug=slug)

    ancestors = list(page.ancestors().reverse())
    edit = (
        request.user.is_authenticated
        and request.user.section_set.filter(pk=article.section.pk).exists()
    )

    return render(
        request,
        article.template.template_name,
        {
            "page": page,
            "article": article,
            "obj": article,
            "edit": edit,
            "header_image": article.get_header_image() or page.get_header_image(),
            "title": article.title,
            "meta_tags": meta_tags([article, page] + ancestors, request=request),
            "regions": Regions.from_item(article, renderer=renderer, timeout=60,),
            "page_regions": Regions.from_item(
                page,
                renderer=pages.renderer.renderer,
                timeout=60,
                inherit_from=ancestors,
            ),
        },
    )


class ArticleSitemap(Sitemap):
    changefreq = "never"

    def __init__(self, blog_page):
        self.page = blog_page
        super().__init__()

    def items(self):
        return articles_for_page(self.page)

    def lastmod(self, obj):
        return obj.edited_date


class ArticleFeed(Feed):

    ttl = 6 * 60

    def get_object(self, request, *args, **kwargs):
        page = page_for_app_request(request)
        page.activate_language(request)
        self.limit = int(request.GET.get("limit", "30"))
        return page

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.site.host + obj.get_absolute_url()

    def feed_url(self, obj):
        return obj.get_absolute_url() + "rss/"

    def description(self, obj):
        return obj.meta_description

    def categories(self, obj):
        if obj.category:
            return obj.category.name
        return [
            x
            for x in articles_for_page(obj).values_list("category__name", flat=True)
            if x is not None
        ]

    def items(self, obj):
        return articles_for_page(obj)[: self.limit]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.tagline

    def item_author_name(self, item):
        if item.author:
            return item.author.full_name
        return ""

    def item_author_email(self, item):
        if item.author:
            return item.author.email
        return ""

    def item_pubdate(self, item):
        return item.publication_date

    def item_updateddate(self, item):
        return item.edited_date

    def item_categories(self, item):
        return [item.category.name] if item.category else None
