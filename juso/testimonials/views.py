from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from feincms3.applications import page_for_app_request, reverse_app
from feincms3.regions import Regions
from feincms3_meta.utils import meta_tags

from juso.pages.renderer import renderer

from .forms import TestimonialForm

# Create your views here.


def validate_testimonial(request, pk):
    pass


def create(request):
    page = page_for_app_request(request)
    page.activate_language(request)

    campaign = page.campaign

    form = TestimonialForm(campaign=campaign)

    if request.POST:
        form = TestimonialForm(request.POST, request.FILES, campaign=campaign)

        if form.is_valid():
            form.save()
            return redirect(
                reverse_app(f"testimonial-{campaign.pk}-{page.site_id}",
                            "index"))

    return render(
        request,
        "testimonials/create_testimonial.html",
        {
            "form":
            form,
            "campaign":
            campaign,
            "page":
            page,
            "regions":
            Regions.from_item(
                page,
                renderer=renderer,
                timeout=60,
                inherit_from=page.ancestors().reverse(),
            ),
        },
    )


def index(request):
    page = page_for_app_request(request)
    page.activate_language(request)

    campaign = page.campaign
    testimonials = campaign.testimonial_set.filter(public=True)

    create_url = reverse_app(f"testimonial-{campaign.pk}-{page.site_id}",
                             "create")
    form = TestimonialForm(campaign=campaign)

    if request.POST:
        form = TestimonialForm(request.POST, request.FILES, campaign=campaign)

        if form.is_valid():
            form.save()
            return redirect(
                reverse_app(f"testimonial-{campaign.pk}-{page.site_id}",
                            "index"))

    paginator = Paginator(testimonials, 26)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    ancestors = list(page.ancestors().reverse())
    return render(
        request,
        "testimonials/testimonial_list.html",
        {
            "campaign":
            campaign,
            "page_obj":
            page_obj,
            "page":
            page,
            "meta_tags":
            meta_tags([page] + ancestors, request=request),
            "create_url":
            create_url,
            "regions":
            Regions.from_item(
                page,
                renderer=renderer,
                timeout=60,
                inherit_from=page.ancestors().reverse(),
            ),
            'form':
            form
        },
    )
