import uuid

from content_editor.models import create_plugin_base
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from feincms3.cleanse import CleansedRichTextField

import phonenumbers
import requests

from juso.forms.forms import get_form_instance

# Create your models here.
from juso.sections.models import ContentMixin, Section, get_template_list

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
    ("honeypot", _("honeypot")),
    ("captcha", _("Captcha")),
)

SIZES = (
    ("one", _("one")),
    ("one-half", _("one half")),
    ("one-third", _("one third")),
    ("one-fourth", _("one fouth")),
    ("three-fourths", _("thre fourths")),
    ("two-thirds", _("two thirds")),
)


class MailchimpConnection(models.Model):
    name = models.CharField(_("name"), max_length=30)
    api_key = models.CharField(_("mailchimp api key"), max_length=180)
    api_server = models.CharField(_("mailchimp api server"), max_length=20)

    section = models.ForeignKey(Section, models.CASCADE)

    def __str__(self):
        return self.name


class Form(ContentMixin):
    TEMPLATES = get_template_list(
        "form",
        ((
            "default",
            ("fields", "handlers"),
        ), ),
    )
    fullwidth = models.BooleanField(_("full width"))
    submit = models.CharField(max_length=200)
    size = models.TextField(_("size"), default="one", choices=SIZES)
    success_message = CleansedRichTextField(_("success message"), blank=True)
    success_redirect = models.URLField(_("success redirect"), blank=True)

    email = models.CharField(_("e-mail"), max_length=1200, blank=True)
    webhook = models.URLField(_("webhook"), max_length=1200, blank=True)
    list_id = models.CharField(_("mailtrain list id"),
                               max_length=30,
                               blank=True)
    webhook_dict = models.JSONField(_("webhook dict"), blank=True, null=True)
    webhooks = models.ManyToManyField("Webhook", blank=True)

    linked_form = models.ForeignKey("self",
                                    models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name="linked_forms")
    linking_field_slug = models.CharField(max_length=30, blank=True)

    mailchimp_connection = models.ForeignKey(MailchimpConnection,
                                             models.SET_NULL,
                                             null=True,
                                             blank=True)
    mailchimp_list_id = models.CharField(_("mailchimp list id"),
                                         max_length=100,
                                         blank=True)
    tags = models.CharField(_("tags"), max_length=30, blank=True)

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
        return (FormEntryValue.objects.filter(
            form_entry__form=self,
            field__slug=field_slug,
        ).aggregate(r=models.Sum("int_value"))["r"] or 0)

    def clear_entries(self):
        self.formentry_set.all().delete()

    def get_fields(self):
        fields = []
        if self.linked_form:
            fields += self.linked_form.get_fields()
        for field in FormField.objects.filter(parent=self):
            fields.append(field.slug)
        return fields

    def entry_dict(self):
        form_entries = []

        fields = self.get_fields()

        for entry in self.formentry_set.all():
            form_entries.append(entry.get_values(fields))

        fields.append("ip")
        fields.append("created")
        fields.append("sid")

        return form_entries, fields


class FormField(models.Model):
    name = models.CharField(_("name"),
                            max_length=140,
                            help_text=_("label for form field"))
    input_type = models.CharField(_("type"),
                                  choices=INPUT_TYPES,
                                  max_length=140,
                                  help_text=_("type of the input field"))
    parent = models.ForeignKey(Form, models.CASCADE)

    slug = models.SlugField(
        help_text=_("name that will be used in export headings"))
    required = models.BooleanField(
        _("required"), help_text=_("force people to provide this value"))
    help_text = models.CharField(_("help text"),
                                 max_length=240,
                                 blank=True,
                                 help_text=_("additional info for people"))
    choices = models.TextField(
        _("choices"),
        blank=True,
        help_text=_("provide the options for a choice field"))
    initial = models.TextField(_("initial"),
                               max_length=240,
                               blank=True,
                               help_text=_("initial value for this field"))
    size = models.TextField(_("size"),
                            default="one",
                            choices=SIZES,
                            help_text=_("proportion of the field"))
    ordering = models.IntegerField(default=10)
    disallow_text = models.CharField(max_length=40, blank=True)

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
    submission_id = models.UUIDField(default=uuid.uuid4)

    def get_values(self, fields, json_safe=False):
        values = dict()

        for field in fields:
            values[field] = ""

        if self.form.linked_form:
            linked_sid = self.fields.filter(
                field__slug=self.form.linking_field_slug)

            if linked_sid.exists():
                other = self.form.linked_form.formentry_set.filter(
                    submission_id=linked_sid[0].value)
                if other.exists():
                    values.update(other[0].get_values(fields, json_safe))

        values.update({
            "ip": self.ip,
            "created": str(self.created) if json_safe else self.created,
            "sid": str(self.submission_id),
        })

        for field in self.fields.all():
            values[field.field.slug] = field.value

        return values

    def __str__(self):
        return f"{self.form.title}: {self.created}"

    class Meta:
        verbose_name = _("form entry")
        verbose_name_plural = _("form entries")


class FormEntryValue(models.Model):
    form_entry = models.ForeignKey(FormEntry,
                                   models.CASCADE,
                                   related_name="fields",
                                   verbose_name=_("fields"))
    field = models.ForeignKey(FormField, models.CASCADE)
    value = models.TextField(_("value"), blank=True, null=True)
    int_value = models.IntegerField(_("int value"), default=0)

    def __str__(self):
        return f"{self.field.name}: {self.value}"

    class Meta:
        verbose_name = _("form entry value")
        verbose_name_plural = _("form entry values")


class Webhook(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=800)

    owner = models.ForeignKey(Section, models.CASCADE)

    def send_webhook(self, entry):
        form = entry.form

        entry_data = entry.get_values(form.get_fields(), json_safe=False)
        data = {}

        for field in self.fields.all():
            data[field.webhook_slug] = field.convert_data(
                entry_data.get(field.form_slug), form)

        print(data)
        requests.post(self.url, data=data)

    def __str__(self):
        return self.name


class WebhookField(models.Model):
    form_slug = models.SlugField(help_text=_("slug of the field in the form"))
    webhook_slug = models.CharField(
        max_length=200,
        help_text=_("name of the field in the request to the webhook"))

    field_converter = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("apply a converter on the user input"))
    field_converter_args = models.CharField(
        max_length=200, blank=True, help_text=_("arguments for the converter"))

    webhook = models.ForeignKey(Webhook, models.CASCADE, related_name="fields")

    def convert_data(self, value, form):
        if self.field_converter == "constant":
            return self.field_converter_args

        if self.field_converter == "phonenumber":
            country, output = [
                x.strip() for x in self.field_converter_args.split(",")
            ]
            parsed = phonenumbers.parse(value, country)

            return phonenumbers.format_number(
                parsed, getattr(phonenumbers.PhoneNumberFormat, output))

        if self.field_converter == "toint":
            return int(value)

        return value
