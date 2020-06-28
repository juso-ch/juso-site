from django.shortcuts import reverse
from django import template
from django.core import serializers
from django.utils.safestring import mark_safe

from juso.sections.models import Category

register = template.Library()


@register.filter
def jsonify(obj, fields=None):
    fields = fields.split(',') if fields else None
    obj = obj if hasattr(obj, '__iter__') else (obj,)
    return serializers.serialize(
        'json', obj,
        fields=fields, use_natural_foreign_keys=True,
        use_natural_primary_keys=True,
    )


@register.simple_tag
def categories(language_code):
    return Category.objects.filter(language_code=language_code)

@register.simple_tag
def edit_url(obj):
    return reverse(
        f'admin:{obj._meta.app_label}_{obj._meta.model_name}',
        args=(obj.pk,)
    )


@register.simple_tag
def logo(category=None):
    if category:
        return reverse('logo', kwargs={
            'language':category.language_code,
            'slug':category.slug
        })
    return reverse('logo', kwargs={
        'language': 'no', 'slug': 'default'
    })


@register.filter
def nbsp(obj):
    return mark_safe(obj.replace('~', '&nbsp;'))
