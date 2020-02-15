from django.shortcuts import render, get_object_or_404

from feincms3.apps import page_for_app_request
from feincms3.regions import Regions
from feincms3.shortcuts import render_list

from feincms3_meta.utils import meta_tags

from juso import pages

from juso.events.renderer import renderer, location_renderer
from juso.events.models import Event, Location

# Create your views here.


def event_list_for_page(page, all_events=False, location=None, category=None):
    qs = Event.objects.filter(
        language_code=page.language_code
    )

    all_events = all_events or page.all_events
    location = location or page.location
    category = category or page.category

    if location:
        qs = qs.filter(location=location)

    if category:
        qs = qs.filter(category=page.category)

    if page.event_namespace:
        qs = qs.filter(namespace=page.event_namespace)

    if hasattr(page.site, 'section') and not all_events:
        qs = qs.filter(section=page.site.section)

    return qs


def location_detail(request, slug, all_events=False):
    page = page_for_app_request(request)
    page.activate_language(request)

    location = get_object_or_404(
        Location.objects.all(),
        slug=slug
    )
    ancestors = page.ancestors().reverse()

    return render(
        request,
        "events/location_detail.html",
        {
            'page': page,
            'location': location,
            'meta_tags': meta_tags(
                [location, page] + ancestors, request=request
            ),
            'regions': Regions.from_item(
                location, renderer=location_renderer, timeout=60,
            ),
            'page_regions': Regions.from_item(
                page, renderer=pages.renderer.renderer,
                timeout=60, inherit_from=ancestors
            )
        }
    )


def event_list(request, all_events=False):
    page = page_for_app_request(request)
    page.activate_language(request)

    ancestors = page.ancestors().reverse()

    return render_list(
        request,
        event_list_for_page(page),
        {
            'page': page,
            'meta_tags': meta_tags(
                [page] + ancestors,
                request=request
            ),
            'regions': Regions.from_item(
                page, renderer=page.renderer.renderer, timeout=60,
                inherit_from=ancestors
            )
        },
        paginate_by=20,
    )


def event_detail(request, slug):
    page = page_for_app_request(request)
    page.activate_language(request)

    event = get_object_or_404(
        event_list_for_page(page),
        slug=slug
    )

    ancestors = list(page.ancestors().reverse())

    return render(
        request,
        event.template.template_name,
        {
            'page': page,
            'event': event,
            'meta_tags': meta_tags(
                [event, page] + ancestors,
                request=request,
            ),
            "regions": Regions.from_item(
                event, renderer=renderer, timout=60,
            ),
            "page_regions": Regions.from_item(
                page, renderer=pages.renderer.renderer,
                timeout=60, inherit_from=ancestors
            )
        },
    )
