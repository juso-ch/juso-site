from django import template
from django.utils.safestring import mark_safe
from django.core import serializers


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

