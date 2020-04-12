from django.shortcuts import render

# Create your views here.


def form_view(request, form):
    # TODO: If post: process form; else: render form

    return render(request, 'forms/form_detail.html', {

    })
