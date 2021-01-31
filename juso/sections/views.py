from django.contrib.sitemaps import Sitemap
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

    category_list = page.categorylinking_set.all()

    edit = (request.user.is_authenticated and
            request.user.section_set.filter(pk=page.site.section.pk).exists())

    ancestors = list(page.ancestors().reverse())

    return render_list(
        request,
        category_list,
        {
            "page":
            page,
            "edit":
            edit,
            "header_image":
            page.get_header_image(),
            "meta_tags":
            meta_tags([page] + ancestors, request=request),
            "regions":
            Regions.from_item(
                page,
                renderer=pages.renderer.renderer,
                timeout=60,
            ),
        },
        paginate_by=100,
    )


def category_detail(request, slug):
    page = page_for_app_request(request)
    page.activate_language(request)

    category = get_object_or_404(Category,
                                 slug=slug,
                                 language_code=page.language_code)

    events = event_list_for_page(page).filter(category=category)
    articles = articles_for_page(page).filter(category=category)
    description = ""

    if page.categorylinking_set.filter(category=category).exists():
        description = page.categorylinking_set.get(
            category=category).description

    page_number = request.GET.get("page", 1)
    articles = Paginator(articles, per_page=12).get_page(page_number)

    ancestors = list(page.ancestors().reverse())

    return render(
        request,
        "sections/category_detail.html",
        {
            "page":
            page,
            "articles":
            articles,
            "events":
            events,
            "category":
            category,
            "obj":
            category,
            "description":
            description,
            "title":
            category.name,
            "header_image":
            category.get_header_image() or page.get_header_image(),
            "meta_tags":
            meta_tags([category, page] + ancestors, request=request),
            "regions":
            Regions.from_item(
                page,
                renderer=pages.renderer.renderer,
                timeout=60,
                inherit_from=ancestors,
            ),
        },
    )


class CategorySitemap(Sitemap):
    changefreq = "monthly"

    def __init__(self, page):
        self.page = page
        super().__init__()

    def items(self):
        return self.page.categorylinking_set.all()
