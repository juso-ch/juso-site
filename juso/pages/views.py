from django.shortcuts import get_object_or_404, render, redirect
from feincms3.regions import Regions
from feincms3_meta.utils import meta_tags

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

    return get_object_or_404(
        Page.objects.active(),
        is_landing_page=True,
    )


def page_detail(request, path=None):
    if path is None and not Page.objects.active().filter(path='/').exists():
        return redirect(get_landing_page(request).path)

    page = get_object_or_404(
        Page.objects.active(),
        path=f"/{path}/" if path else '/',
    )
    page.activate_language(request)
    ancestors = list(page.ancestors().reverse())
    return render(
        request,
        page.template.template_name,
        {
            "page": page,
            "meta_tags": meta_tags([page] + ancestors, request=request),
            "regions": Regions.from_item(
                page, renderer=renderer, timeout=60,
                inherit_from=page.ancestors().reverse(),
            ),
        },
    )
