from content_editor.models import create_plugin_base
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from feincms3.cleanse import CleansedRichTextField

from juso.forms.forms import get_form_instance

# Create your models here.
from juso.sections.models import ContentMixin, get_template_list

INPUT_TYPES = (
    ("text", _("text")),
    ("long_text", _("long text")),
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

    email = models.CharField(_("e-mail"), max_length=1200, blank=True)
    webhook = models.URLField(_("webhook"), max_length=1200, blank=True)
    list_id = models.CharField(_("list id"), max_length=30, blank=True)
    webhook_dict = models.JSONField(_("webhook dict"), blank=True)

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

    def aggregate(self, field_slug):
        return (
            FormEntryValue.objects.filter(
                form_entry__form=self, field__slug=field_slug,
            ).aggregate(r=models.Sum("int_value"))["r"]
            or 0
        )

    def entry_dict(self):
        form_entries = []
        fields = set()

        for field in FormField.objects.filter(parent=self):
            fields.add(field.slug)

        for entry in self.formentry_set.all():
            values = {"ip": entry.ip, "created": entry.created}

            for field in fields:
                value = entry.fields.filter(field__slug=field)
                if value.exists():
                    values[field] = value[0].value
                else:
                    values[field] = ""

            form_entries.append(values)

        fields.add("ip")
        fields.add("created")

        return form_entries, fields


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

    unique = models.BooleanField(
        _("unique"),
        default=False,
        help_text=_("restricts people to only submit one value for this form"),
    )

    unique_error = models.CharField(
        _("unique error"),
        blank=True,
        max_length=180,
        help_text=_("error that is displayed if value already exists"),
    )

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
    value = models.TextField(_("value"), blank=True, null=True)
    int_value = models.IntegerField(_("int value"), default=0)

    def __str__(self):
        return f"{self.field.name}: {self.value}"

    class Meta:
        verbose_name = _("form entry value")
        verbose_name_plural = _("form entry values")
