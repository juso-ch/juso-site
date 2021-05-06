from django.shortcuts import render
from feincms3.applications import page_for_app_request
from feincms3_meta.utils import meta_tags

# Create your views here.


def collection_view(request):
    page = page_for_app_request(request)
    collection = page.collection

    ancestors = list(page.ancestors().reverse())

    return render(
        request,
        "link_collections/collection.html",
        {
            "meta_tags": meta_tags([page] + ancestors, request=request),
            "page": page,
            "collection": collection,
        },
    )
