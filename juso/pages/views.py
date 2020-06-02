from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.contrib.sitemaps import Sitemap
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from feincms3.regions import Regions
from feincms3_meta.utils import meta_tags
from feincms3_sites.middleware import current_site

from juso.blog.views import ArticleSitemap
from juso.events.views import EventSitemap
from juso.sections.views import CategorySitemap
from juso.pages.models import Page
from juso.pages.renderer import renderer

# Create your views here.


def get_landing_page(request):
    queryset = Page.objects.active().filter(
        is_landing_page=True,
        language_code=request.LANGUAGE_CODE
    )

    if queryset.exists():
        return queryset[0]

    return get_list_or_404(
        Page.objects.active(),
        is_landing_page=True,
    )[0]


@ensure_csrf_cookie
def page_detail(request, path=None):
    if path is None and not Page.objects.active().filter(path='/').exists():
        return redirect(get_landing_page(request).path)

    page = get_object_or_404(
        Page.objects.active(),
        path=f"/{path}/" if path else '/',
    )

    if page.redirect_to_url or page.redirect_to_page:
        return redirect(page.redirect_to_url or page.redirect_to_page)

    edit = request.user.is_authenticated and\
            request.user.section_set.filter(pk=page.site.section.pk).exists()

    page.activate_language(request)
    ancestors = list(page.ancestors().reverse())
    return render(
        request,
        page.template.template_name,
        {
            "page": page,
            "edit": edit,
            "header_image": page.get_header_image(),
            "meta_tags": meta_tags([page] + ancestors, request=request),
            "regions": Regions.from_item(
                page, renderer=renderer, timeout=60,
            ),
        },
    )


def error404(request, exception):
    print("Hello")
    return render(
        request, '404.html', {
            'exception': exception
        }
    )


def error500(request):
    return render(
        request, '500.html'
    )

def webmanifest(request):
    page = get_landing_page(request) or get_object_or_404(
        Page.objects.active(),
        path='/',
    )

    return render(request, 'manifest.webmanifest', {
        'page': page,
        'color': settings.DEFAULT_COLOR,
    })


def service_worker(request):
    return render(request, 'service-worker.js', {

    }, content_type="text/javascript")


def offline_view(request):
    page = get_landing_page(request) or get_object_or_404(
        Page.objects.active(),
        path='/',
    )

    return render(request, 'offline.html', {
        'page': page,
        'color': settings.DEFAULT_COLOR,
    })

def sitemap_index(request, path='/'):
    sitemaps = {}

    top_page = get_object_or_404(
        Page.objects.active(),
        path=f"/{path}/" if path else '/',
    )

    sitemaps['pages'] = PageSitemap(top_page)

    for blog_page in top_page.descendants(include_self=True).filter(application='blog'):
        sitemaps[blog_page.slug] = ArticleSitemap(blog_page)

    for event_page in top_page.descendants(include_self=True).filter(application='events'):
        sitemaps[event_page.slug] = EventSitemap(event_page)

    for category_page in top_page.descendants(include_self=True).filter(application='categories'):
        sitemaps[category_page.slug] = CategorySitemap(category_page)

    return sitemap_view(
        request, sitemaps,
    )


class PageSitemap(Sitemap):

    changefreq = 'monthly'

    def __init__(self, top_page):
        self.top_page = top_page
        super().__init__()

    def items(self):
        return self.top_page.descendants(include_self=True)

    def lastmod(self, obj):
        return obj.lastmod
