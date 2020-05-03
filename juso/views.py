from django.shortcuts import render
from juso.sections.models import Category

def logo(request, slug, language):
    color = '#fff'
    category = Category.objects.filter(slug=slug, language_code=language)

    if category.exists():
        color = category[0].color or color

    return render(request, 'logo.svg', {
        'color': color
    }, content_type="image/svg+xml")
