from django.shortcuts import render, get_object_or_404
from feincms3.regions import Regions

from juso.pages.models import Page
from juso.pages.renderer import renderer

# Create your views here.


def page_detail(request, path=None):
    page = get_object_or_404(
        Page.objects.active(),
        path="/{}/".format(path) if path else "/",
    )
    page.activate_language(request)
    return render(
        request,
        "pages/default.html",
        {
            "page": page,
            "regions": Regions.from_item(
                page, renderer=renderer, timeout=60
            ),
        },
    )
