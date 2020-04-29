from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from feincms3.apps import page_for_app_request
from feincms3.regions import Regions
from feincms3.shortcuts import render_list
from feincms3_meta.utils import meta_tags

from juso import pages
from juso.search import consume
from juso.glossary.models import Entry
# Create your views here.


def glossary(request):
    page = page_for_app_request(request)
    page.activate_language(request)

    ancestors = list(page.ancestors().reverse())

    entries = Entry.objects.filter(language_code=page.language_code)
    q = ''

    if 'q' in request.GET and request.GET['q']:
        vector = SearchVector('name', weight='A')\
                + SearchVector('content', weight='B')
        query = consume(request.GET['q'])
        print(query)
        q = request.GET['q']
        print(q)

        entries = entries.annotate(
            rank=SearchRank(vector, query)
        ).filter(rank__gte=0.1).order_by('-rank')


    return render_list(
        request,
        entries,
        {
            'page': page,
            'meta_tags': meta_tags([page] + ancestors, request=request),
            'header_image': page.get_header_image(),
            'regions': Regions.from_item(
                page, renderer=pages.renderer.renderer, timeout=60,
                inherit_from=ancestors
            ),
            'search': q
        },
        paginate_by=50
    )
