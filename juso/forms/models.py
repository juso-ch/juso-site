from content_editor.models import create_plugin_base
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from feincms3 import plugins
from feincms3.apps import apps_urlconf, reverse_app
from feincms3.cleanse import CleansedRichTextField
from feincms3.mixins import TemplateMixin
from feincms3_sites.middleware import current_site, set_current_site

from juso.forms.forms import get_form_instance

# Create your models here.
from juso.sections.models import ContentMixin, get_template_list
from juso.utils import number_word

INPUT_TYPES = (
    ("text", _("text")),
    ("email", _("email")),
    ("boolean", _("boolean")),
    ("date", _("date")),
    ("datetime", _("datetime")),
    ("time", _("time")),
    ("decimal", _("decimal")),
    ("file", _("file")),
    ("image", _("image")),
    ("int", _("integer")),
    ("choice", _("choice")),
    ("multi", _("multiple choice")),
    ("url", _("url")),
    ("hidden", _("hidden")),
    ("section", _("section")),
)


SIZES = (
    ("one", _("one")),
    ("one-half", _("one half")),
    ("one-third", _("one third")),
    ("one-fourth", _("one fouth")),
    ("three-fourths", _("thre fourths")),
    ("two-thirds", _("two thirds")),
)


class Form(ContentMixin):
    TEMPLATES = get_template_list("form", (("default", ("fields", "handlers"),),))
    fullwidth = models.BooleanField(_("full width"))
    submit = models.CharField(max_length=200)
    size = models.TextField(_("size"), default="one", choices=SIZES)
    success_message = CleansedRichTextField(_("success message"), blank=True)
    success_redirect = models.URLField(_("success redirect"), blank=True)

    email = models.EmailField(_("e-mail"), blank=True)
    webhook = models.URLField(_("webhook"), max_length=1200, blank=True)

    def get_instance(self, request):
        return get_form_instance(self, request)

    class Meta:
        verbose_name = _("form")
        verbose_name_plural = _("forms")
        ordering = ["title"]

    def get_absolute_url(self):
        return reverse("forms:form-detail", kwargs={"pk": self.pk})

    def count(self):
        return self.formentry_set.count()


PluginBase = create_plugin_base(Form)


class FormField(PluginBase):
    name = models.CharField(_("name"), max_length=140)
    input_type = models.CharField(_("type"), choices=INPUT_TYPES, max_length=140)

    slug = models.SlugField()
    required = models.BooleanField(_("required"))
    help_text = models.CharField(_("help text"), max_length=240, blank=True)
    choices = models.TextField(_("choices"), blank=True)
    initial = models.TextField(_("initial"), max_length=240, blank=True)
    size = models.TextField(_("size"), default="one", choices=SIZES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("form field")
        verbose_name_plural = _("form fields")
        ordering = ["ordering"]
        indexes = [models.Index(fields=("parent", "slug"))]


class FormEntry(models.Model):
    form = models.ForeignKey(Form, models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    ip = models.GenericIPAddressField(_("ip address"), blank=True, null=True)

    def __str__(self):
        return f"{self.form.title}: {self.created}"

    class Meta:
        verbose_name = _("form entry")
        verbose_name_plural = _("form entries")


class FormEntryValue(models.Model):
    form_entry = models.ForeignKey(
        FormEntry, models.CASCADE, related_name="fields", verbose_name=_("fields")
    )
    field = models.ForeignKey(FormField, models.CASCADE)
    value = models.TextField(_("value"), blank=True)

    def __str__(self):
        return f"{self.field.name}: {self.value}"

    class Meta:
        verbose_name = _("form entry value")
        verbose_name_plural = _("form entry values")
