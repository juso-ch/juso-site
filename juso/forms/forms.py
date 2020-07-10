from __future__ import annotations

from types import MethodType

from django import forms
from django.forms import widgets

from juso.forms import models
from juso.sections.models import Section


class DynamicForm(forms.Form):
    def __init__(self, *args, form: models.Form, request, **kwargs):
        self.form = form
        self.request = request
        super().__init__(*args, **kwargs)

        for field in self.form.forms_formfield_set.all():
            self.fields[field.slug] = get_field_instance(field, request)
            if field.unique:
                bound_field = field

                def clean_field(self):
                    values = models.FormEntryValue.objects.filter(
                        form_entry__form=self.form,
                        field=bound_field,
                        value=self.cleaned_data[bound_field.slug],
                    )

                    if values.exists():
                        raise forms.ValidationError(bound_field.unique_error)
                    return self.cleaned_data[bound_field.slug]

                self.__dict__[f"clean_{field.slug}"] = MethodType(clean_field, self)


class HiddenField(forms.Field):
    widget = forms.HiddenInput


class DateField(forms.DateField):
    widget = forms.DateInput(attrs={"type": "date"})


class DateTimeField(forms.DateTimeField):
    widget = forms.DateTimeInput(attrs={"type": "datetime"})


class CustomChoiceField(forms.ChoiceField):
    widget = widgets.ChoiceWidget


class TextField(forms.CharField):
    widget = widgets.Textarea


def get_form_instance(form: models.Form, request=None):
    """
    Returns a `forms.Form` instance  with the fields
    defined by the `models.Form` instance.
    """
    dynamic_form = DynamicForm(request=request, form=form)

    if request and request.POST:
        dynamic_form = DynamicForm(request=request, form=form, data=request.POST)

    return dynamic_form


def get_field_instance(field, request):
    """
    Returns a `forms.FormField` instance as defined by
    the given field.
    """
    cls = get_field_class(field.input_type)

    if field.input_type in ["choice", "multi"]:
        instance = cls(
            required=field.required,
            label=field.name,
            help_text=field.help_text,
            choices=((l.strip(), l.strip()) for l in field.choices.split("\n")),
            initial=field.initial,
        )
    elif field.input_type == "section":
        instance = cls(
            required=field.required,
            label=field.name,
            help_text=field.help_text,
            initial=field.initial,
            queryset=Section.objects.filter(
                name__in=(l.strip() for l in field.choices.split("\n"))
            )
            if field.choices
            else Section.objects.all(),
        )
    else:
        instance = cls(
            required=field.required,
            label=field.name,
            help_text=field.help_text,
            initial=field.initial,
        )
    instance.size = field.size

    return instance


INPUT_TYPES = {
    "text": forms.CharField,
    "long_text": TextField,
    "boolean": forms.BooleanField,
    "choice": forms.ChoiceField,
    "date": DateField,
    "datetime": DateTimeField,
    "decimal": forms.DecimalField,
    "email": forms.EmailField,
    "file": forms.FileField,
    "float": forms.FloatField,
    "image": forms.ImageField,
    "int": forms.IntegerField,
    "multi": forms.MultipleChoiceField,
    "time": forms.TimeField,
    "url": forms.URLField,
    "hidden": HiddenField,
    "section": forms.ModelChoiceField,
}


def get_field_class(input_type):
    return INPUT_TYPES.get(input_type)
