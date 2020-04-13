from django.shortcuts import render, get_object_or_404

from juso.forms import models
# Create your views here.


def form_view(request, form):
    # TODO: If post: process form; else: render form
    form = get_object_or_404(models.Form, pk=form).get_instance(request)

    if request.POST:
        return process_form(request, form)

    return render(request, 'forms/form_detail.html', {
        'form': form
    })


def process_form(request, form):
    pass
