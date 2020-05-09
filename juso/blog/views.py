from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from feincms3.apps import page_for_app_request
from feincms3.regions import Regions
from feincms3.shortcuts import render_list
from feincms3_meta.utils import meta_tags

from juso import pages
from juso.sections.models import Category
from juso.blog import models
from juso.search import consume
from juso.blog.renderer import renderer

# Create your views here.


def articles_for_page(page, qs=None):
    qs = qs if qs else models.Article.objects.filter(
        language_code=page.language_code
    )

    if page.category:
        qs = qs.filter(category=page.category)

    if page.blog_namespace:
        qs = qs.filter(namespace=page.blog_namespace)

    if page.sections.exists():
        qs = qs.filter(section__in=page.sections.all())
    elif hasattr(page.site, 'section'):
        qs = qs.filter(section=page.site.section)

    return qs.filter(publication_date__lte=timezone.now())


def article_list(request):
    page = page_for_app_request(request)
    page.activate_language(request)

    article_list = articles_for_page(page)
    category_list = Category.objects.filter(
        article__in=article_list
    ).distinct()

    if request.GET.get('category', None):
        article_list = article_list.filter(
            category__slug__in=request.GET.getlist('category')
        )

    if request.GET.get('search', ''):
        vector = SearchVector('title', weight='A')\
                + SearchVector('category', weight='B')\
                + SearchVector('blog_richtext_set__text', weight='A')\
                + SearchVector('blog_glossaryrichtext_set__text', weight='A')
        query = consume(request.GET['search'])
        q = request.GET['search']
        article_list = article_list.annotate(
            rank=SearchRank(vector, query)
        ).filter(rank__gte=0.1).order_by('-rank')

    ancestors = list(page.ancestors().reverse())
    return render_list(
        request,
        article_list,
        {
            'page': page,
            'header_image': page.get_header_image(),
            'category_list': category_list,
            "meta_tags": meta_tags([page] + ancestors, request=request),
            'regions': Regions.from_item(
                page, renderer=pages.renderer.renderer, timeout=60,
                inherit_from=ancestors
            )
        },
        paginate_by=12,
    )


def category_list(request, slug):
    page = page_for_app_request(request)
    page.activate_language(request)

    articles = articles_for_page(page).filter(
        category__slug=slug
    )

    ancestors = list(page.ancestors().reverse())

    return render_list(
        request,
        articles,
        {
            'page': page,
            'header_image': page.get_header_image(),
            "meta_tags": meta_tags([page] + ancestors, request=request),
            'regions': Regions.from_item(
                page, renderer=pages.renderer.renderer, timeout=60,
                inherit_from=ancestors
            )
        },
        paginate_by=10,
    )


def article_detail(request, slug):
    page = page_for_app_request(request)
    page.activate_language(request)

    article = get_object_or_404(
        articles_for_page(page),
        slug=slug
    )

    ancestors = list(page.ancestors().reverse())
    edit = request.user.is_authenticated and \
            request.user.section_set.filter(pk=article.section.pk).exists()

    return render(
        request,
        article.template.template_name,
        {
            "page": page,
            "article": article,
            "obj": article,
            'edit': edit,
            'header_image': article.get_header_image() or page.get_header_image(),
            "title": article.title,
            "meta_tags": meta_tags(
                [article, page] + ancestors,
                request=request
            ),
            "regions": Regions.from_item(
                article, renderer=renderer, timeout=60,
            ),
            "page_regions": Regions.from_item(
                page, renderer=pages.renderer.renderer,
                timeout=60, inherit_from=ancestors)
        },
    )
