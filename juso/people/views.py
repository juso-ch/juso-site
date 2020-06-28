from django.shortcuts import get_object_or_404, render
from feincms3.apps import page_for_app_request
from feincms3.regions import Regions
from feincms3.shortcuts import render_list
from feincms3_meta.utils import meta_tags

from juso import pages
from juso.people.models import Person, Team

# Create your views here.


def person_detail(request, pk):
    page = page_for_app_request(request)
    page.activate_language(request)

    person = get_object_or_404(Person, pk=pk)

    memberships = person.membership_set.filter(team__language_code=page.language_code)

    ancestors = list(page.ancestors().reverse())

    return render(
        request,
        "people/person_detail.html",
        {
            "page": page,
            "person": person,
            "memberships": memberships,
            "meta_tags": meta_tags([page] + ancestors, request=request),
            "regions": Regions.from_item(
                page,
                renderer=pages.renderer.renderer,
                timeout=60,
                inherit_from=ancestors,
            ),
        },
    )


def team_detail(request, pk):
    page = page_for_app_request(request)
    page.activate_language(request)

    team = get_object_or_404(Team, pk=pk)

    ancestors = list(page.ancestors().reverse())

    return render(
        request,
        "people/team_detail.html",
        {
            "page": page,
            "team": team,
            "meta_tags": meta_tags([page] + ancestors, request=request),
            "regions": Regions.from_item(
                page,
                renderer=pages.renderer.renderer,
                timeout=60,
                inherit_from=ancestors,
            ),
        },
    )


def teams_for_section(request):
    page = page_for_app_request(request)
    page.activate_language(request)

    section = page.site.section
    ancestors = list(page.ancestors().reverse())

    return render_list(
        request,
        Team.objects.filter(section=section, language_code=page.language_code,),
        {
            "page": page,
            "meta_tags": meta_tags([page] + ancestors, request=request),
            "regions": Regions.from_item(
                page,
                renderer=pages.renderer.renderer,
                timeout=60,
                inherit_from=ancestors,
            ),
        },
        paginate_by=10,
    )
