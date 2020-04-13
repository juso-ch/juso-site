from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from feincms3.apps import page_for_app_request
from feincms3.regions import Regions
from feincms3.shortcuts import render_list
from feincms3_meta.utils import meta_tags

from juso import pages
from juso.blog.views import articles_for_page
from juso.events.views import event_list_for_page
from juso.sections.models import Category


def category_list(request):
    page = page_for_app_request(request)
    page.activate_language(request)

    events = event_list_for_page(page)
    articles = articles_for_page(page)

    categories = Category.objects.filter(
        Q(event__in=events) | Q(article__in=articles)
    ).exclude(pk__in=page.featured_categories.all()).distinct()

    featured_categories = page.featured_categories.all()

    for category in featured_categories:
        category.events = events.filter(category=category)[:5]
        category.articles = articles.filter(category=category)[:4]

    ancestors = list(page.ancestors().reverse())

    return render_list(
        request,
        categories,
        {
            'page': page,
            'featured_categories': featured_categories,
            'all_categories': categories.all(),
            "meta_tags": meta_tags([page] + ancestors, request=request),
            'regions': Regions.from_item(
                page, renderer=pages.renderer.renderer, timeout=60,
            )
        },
        paginate_by=10,
    )


def category_detail(request, slug):
    page = page_for_app_request(request)
    page.activate_language(request)

    category = get_object_or_404(
        Category, slug=slug, language_code=page.language_code
    )

    events = event_list_for_page(page).filter(category=category)
    articles = articles_for_page(page).filter(category=category)

    page_number = request.GET.get('page', 1)
    articles = Paginator(articles, per_page=6).get_page(page_number)

    ancestors = list(page.ancestors().reverse())

    return render(
        request,
        'sections/category_detail.html',
        {
            "page": page,
            "articles": articles,
            "events": events,
            "category": category,
            "title": category.name,
            "meta_tags": meta_tags(
                [category, page] + ancestors,
                request=request
            ),
            "regions": Regions.from_item(
                page, renderer=pages.renderer.renderer,
                timeout=60, inherit_from=ancestors)
        },
    )
