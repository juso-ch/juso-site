from django.shortcuts import get_object_or_404, render

from feincms3.shortcuts import render_list
from feincms3.apps import page_for_app_request

from feincms3.regions import Regions
from juso.blog import models
from juso.blog.renderer import renderer
from juso import pages

# Create your views here.


def articles_for_page(page, qs=None):
    qs = qs if qs else models.Article.objects.all()
    if page.category:
        qs = qs.filter(category=page.category)
    if page.blog_namespace:
        qs = qs.filter(namespace=page.blog_namespace)
    if hasattr(page.site, 'section'):
        qs = qs.filter(section=page.site.section)
    return qs


def article_list(request):
    print(type(request.urlconf))
    page = page_for_app_request(request)
    page.activate_language(request)

    return render_list(
        request,
        articles_for_page(page),
        {
            'page': page,
            'regions': Regions.from_item(
                page, renderer=pages.renderer.renderer, timeout=60
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

    return render(
        request,
        article.template.template_name,
        {
            "page": page,
            "article": article,
            "regions": Regions.from_item(
                article, renderer=renderer, timeout=60
            ),
            "page_regions": Regions.from_item(
                page, renderer=pages.renderer.renderer, timeout=60
            ),
        },
    )
