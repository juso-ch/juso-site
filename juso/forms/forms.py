from __future__ import annotations

from django import forms
from juso.forms import models


class DynamicForm(forms.Form):

    def __init__(self, *args, form: models.Form, request, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = form
        self.request = request

        for field in form.forms_formfield_set.all():
            self.fields[field.slug] = get_field_instance(
                field, request
            )


class HiddenField(forms.Field):
    widget = forms.HiddenInput


def get_form_instance(form: models.Form, request=None):
    """
    Returns a `forms.Form` instance  with the fields
    defined by the `models.Form` instance.
    """
    form = DynamicForm(request=request, form=form)

    if request and request.POST:
        form = DynamicForm(
            request=request,
            form=form,
            data=request.POST
        )

    return form


def get_field_instance(field, request):
    """
    Returns a `forms.FormField` instance as defined by
    the given field.
    """
    cls = get_field_class(field.input_type)

    if field.input_type in ['choice', 'multi']:
        instance = cls(
            required=field.required,
            help_text=field.help_text,
            choices=field.choices.split('\n'),
            initial=field.initial,
        )
    else:
        instance = cls(
            required=field.required,
            help_text=field.help_text,
            initial=field.initial,
        )

    if request and field.slug in request.GET:
        instance.initial = request.GET.get(field.slug)

    return instance


INPUT_TYPES = {
    'text': forms.CharField,
    'boolean': forms.BooleanField,
    'choice': forms.ChoiceField,
    'date': forms.DateField,
    'datetime': forms.DateTimeField,
    'decimal': forms.DecimalField,
    'email': forms.EmailField,
    'file': forms.FileField,
    'float': forms.FloatField,
    'image': forms.ImageField,
    'int': forms.IntegerField,
    'multi': forms.MultipleChoiceField,
    'time': forms.TimeField,
    'url': forms.URLField,
    'hidden': HiddenField
}


def get_field_class(input_type):
    return INPUT_TYPES.get(input_type)
