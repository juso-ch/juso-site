from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import ensure_csrf_cookie
from feincms3.regions import Regions
from feincms3_meta.utils import meta_tags
from feincms3_sites.middleware import current_site

from juso.blog.models import Article
from juso.blog.views import ArticleSitemap
from juso.events.views import EventSitemap
from juso.pages.models import Page
from juso.pages.renderer import renderer
from juso.sections.views import CategorySitemap

# Create your views here.


def get_landing_page(request):
    queryset = Page.objects.active().filter(
        is_landing_page=True, language_code=request.LANGUAGE_CODE)

    if bool(queryset):
        return queryset[0]

    return get_list_or_404(
        Page.objects.active(),
        is_landing_page=True,
    )[0]


@ensure_csrf_cookie
def page_detail(request, path=None):
    page = Page.objects.active().filter(path=f"/{path}/" if path else "/")

    if path is None and not bool(page):
        return redirect(
            get_landing_page(request).path +
            (("?" + request.GET.urlencode()) if request.GET else ""))

    if not bool(page):
        page = Page.objects.active().filter(
            path=f"/{request.LANGUAGE_CODE}/{path}/")
        if bool(page):
            return redirect(page[0].path + (
                ("?" + request.GET.urlencode()) if request.GET else ""))

        for language_code, _ in settings.LANGUAGES:
            page = Page.objects.active().filter(
                path=f"/{language_code}/{path}/")

            if bool(page):
                return redirect(page[0].path + (
                    ("?" + request.GET.urlencode()) if request.GET else ""))
        raise Http404()

    page = page[0]

    if page.redirect_to_url or page.redirect_to_page:
        return redirect(
            page.redirect_to_url
            or (page.redirect_to_page.get_absolute_url() +
                (("?" + request.GET.urlencode()) if request.GET else "")))

    edit = (request.user.is_authenticated and
            request.user.section_set.filter(pk=page.site.section.pk).exists())

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
                page,
                renderer=renderer,
                timeout=60,
            ),
        },
    )


def error404(request, exception):
    query = Article.objects.filter(
        slug=[x for x in request.path.split("/") if x][-1])

    if bool(query):
        return redirect(query[0].get_absolute_url())

    try:
        page = get_landing_page(request)
    except Http404:
        page = Page.objects.first()
    page.activate_language(request)

    return render(
        request,
        "404.html",
        {
            "exception": exception,
            "page": page,
            "regions": Regions.from_item(
                page,
                renderer=renderer,
                timeout=60,
            ),
            "header_image": page.get_header_image(),
        },
    )


def error500(request):
    try:
        page = get_landing_page(request)
    except Http404:
        page = Page.objects.first()
    page.activate_language(request)
    page.activate_language(request)
    return render(
        request,
        "500.html",
        {
            "page": page,
            "regions": Regions.from_item(
                page,
                renderer=renderer,
                timeout=60,
            ),
            "header_image": page.get_header_image(),
        },
    )


def webmanifest(request):
    page = get_landing_page(request) or get_object_or_404(
        Page.objects.active(),
        path="/",
    )

    return render(
        request,
        "manifest.webmanifest",
        {
            "page": page,
            "color": page.primary_color or settings.DEFAULT_COLOR,
        },
    )


def service_worker(request):
    return render(request,
                  "service-worker.js", {},
                  content_type="text/javascript")


def offline_view(request):
    page = get_landing_page(request) or get_object_or_404(
        Page.objects.active(),
        path="/",
    )

    return render(
        request,
        "offline.html",
        {
            "page": page,
            "color": settings.DEFAULT_COLOR,
        },
    )


def sitemap_index(request, path=None):
    sitemaps = {}

    top_page = get_object_or_404(
        Page.objects.active(),
        path=f"/{path}/" if path else "/",
    )

    sitemaps["pages"] = PageSitemap(top_page)

    for blog_page in top_page.descendants(include_self=True).filter(
            application="blog"):
        sitemaps[blog_page.slug] = ArticleSitemap(blog_page)

    for event_page in top_page.descendants(include_self=True).filter(
            application="events"):
        sitemaps[event_page.slug] = EventSitemap(event_page)

    for category_page in top_page.descendants(include_self=True).filter(
            application="categories"):
        sitemaps[category_page.slug] = CategorySitemap(category_page)

    return sitemap_view(
        request,
        sitemaps,
    )


class PageSitemap(Sitemap):

    changefreq = "monthly"

    def __init__(self, top_page):
        self.top_page = top_page
        super().__init__()

    def items(self):
        return self.top_page.descendants(include_self=True).filter(
            is_active=True, redirect_to_url="", redirect_to_page__isnull=True)

    def lastmod(self, obj):
        return obj.lastmod
