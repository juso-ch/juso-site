from django.shortcuts import get_object_or_404, render
from feincms3.apps import page_for_app_request
from feincms3.regions import Regions
from feincms3.shortcuts import render_list
from feincms3_meta.utils import meta_tags

from juso import pages
from juso.blog import models
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

    return qs


def article_list(request):
    page = page_for_app_request(request)
    page.activate_language(request)

    ancestors = list(page.ancestors().reverse())
    return render_list(
        request,
        articles_for_page(page),
        {
            'page': page,
            "meta_tags": meta_tags([page] + ancestors, request=request),
            'regions': Regions.from_item(
                page, renderer=pages.renderer.renderer, timeout=60,
                inherit_from=ancestors
            )
        },
        paginate_by=10,
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

    return render(
        request,
        article.template.template_name,
        {
            "page": page,
            "article": article,
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
