from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from feincms3.apps import page_for_app_request
from feincms3.regions import Regions
from feincms3.shortcuts import render_list
from feincms3_meta.utils import meta_tags

from juso import pages
from juso.events.models import Event, Location
from juso.events.renderer import location_renderer, renderer
from juso.sections.models import Section

# Create your views here.


def event_list_for_page(page, past_events=False):
    qs = Event.objects.filter(
        language_code=page.language_code,
    )
    if not past_events:
        qs = qs.filter(end_date__gte=timezone.now())

    category = page.category

    if category:
        qs = qs.filter(category=page.category)

    if page.event_namespace:
        qs = qs.filter(namespace=page.event_namespace)

    if page.sections.exists():
        qs = qs.filter(section__in=page.sections.all())
    elif hasattr(page.site, 'section'):
        qs = qs.filter(section=page.site.section)

    return qs


def location_detail(request, slug):
    page = page_for_app_request(request)
    page.activate_language(request)

    location = get_object_or_404(
        Location.objects.all(),
        slug=slug
    )
    ancestors = list(page.ancestors().reverse())

    return render(
        request,
        "events/location_detail.html",
        {
            'page': page,
            'location': location,
            'obj': location,
            'title': location.name,
            'header_image': location.get_header_image() or page.get_header_image(),
            'event_list': location.event_set.filter(
                end_date__gte=timezone.now(),
            ),
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


def event_list(request):
    page = page_for_app_request(request)
    page.activate_language(request)

    ancestors = list(page.ancestors().reverse())

    event_list = event_list_for_page(page)

    if 'section' in request.GET:
        event_list = event_list.filter(section__slug=request.GET['section'])

    return render_list(
        request,
        event_list,
        {
            'location_list': Location.objects.filter(
                event__in=event_list,
            ).distinct(),
            'page': page,
            'header_image': page.get_header_image(),
            'meta_tags': meta_tags(
                [page] + ancestors,
                request=request
            ),
            'regions': Regions.from_item(
                page, renderer=pages.renderer.renderer, timeout=60,
                inherit_from=ancestors
            )
        },
        paginate_by=12,
    )


def event_detail(request, year, month, day, slug):
    page = page_for_app_request(request)
    page.activate_language(request)

    event = get_object_or_404(
        event_list_for_page(page, past_events=True),
        slug=slug, section=page.site.section,
        start_date__year=year,
        start_date__month=month,
        start_date__day=day,
    )

    ancestors = list(page.ancestors().reverse())

    return render(
        request,
        event.template.template_name,
        {
            'page': page,
            'event': event,
            'obj': event,
            'header_image': event.get_header_image() or page.get_header_image(),
            'title': event.title,
            'meta_tags': meta_tags(
                [event, page] + ancestors,
                request=request,
            ),
            "regions": Regions.from_item(
                event, renderer=renderer, timeout=60,
            ),
            "page_regions": Regions.from_item(
                page, renderer=pages.renderer.renderer,
                timeout=60, inherit_from=ancestors
            )
        },
    )


def event_list_for_section(request, pk):
    page = page_for_app_request(request)
    page.activate_language(request)

    section = get_object_or_404(Section, pk)

    event_list = event_list_for_page(page)

    event_list = event_list.filter(section=section)

    ancestors = list(page.ancestors().reverse())

    return render_list(
        request,
        event_list_for_page(page),
        {
            'page': page,
            'header_image': page.get_header_image(),
            'meta_tags': meta_tags(
                [page] + ancestors,
                request=request
            ),
            'regions': Regions.from_item(
                page, renderer=pages.renderer.renderer, timeout=60,
                inherit_from=ancestors
            ),
            'section': section
        },
        paginate_by=20,
    )
