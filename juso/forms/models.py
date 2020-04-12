from content_editor.models import create_plugin_base

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from feincms3 import plugins
from feincms3.mixins import TemplateMixin

# Create your models here.
from juso.sections.models import get_template_list, ContentMixin
from juso.forms.forms import get_form_instance

INPUT_TYPES = (
    ('text', _("text")),
    ('email', _("email")),
    ('boolean', _("boolean")),
    ('date', _("date")),
    ('datetime', _("datetime")),
    ('time', _("time")),
    ('decimal', _("decimal")),
    ('file', _("file")),
    ('image', _("image")),
    ('int', _("integer")),
    ('choice', _("choice")),
    ('multi', _("multiple choice")),
    ('url', _("url")),
    ('hidden', _("hidden")),
)


class Form(ContentMixin):
    TEMPLATES = get_template_list('form', (
        (
            'default', ('fields', 'handlers'),
        ),
    ))

    submit = models.CharField(max_length=200)
    success_message = models.TextField(_("success message"), blank=True)
    success_redirect = models.URLField(_("success redirect"), blank=True)

    def get_instance(self, request):
        return get_form_instance(self, request)

    class Meta:
        verbose_name = _("form")
        verbose_name_plural = _("forms")
        ordering = ['title']


PluginBase = create_plugin_base(Form)


class RichText(plugins.richtext.RichText, PluginBase):
    class Meta:
        verbose_name = _("rich text")
        verbose_name = _("rich text")


class FormField(PluginBase):
    name = models.CharField(_("name"), max_length=140)
    input_type = models.CharField(
        _("type"), choices=INPUT_TYPES,
        max_length=140
    )
    slug = models.SlugField()
    required = models.BooleanField(_("required"))
    help_text = models.CharField(_("help text"), max_length=240, blank=True)
    choices = models.TextField(_("choices"), blank=True)
    initial = models.TextField(_("initial"), max_length=240, blank=True)


class FormEntry(models.Model):
    form = models.ForeignKey(Form, models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    ip = models.GenericIPAddressField(_("ip address"), blank=True, null=True)


class FormEntryValue(models.Model):
    form_entry = models.ForeignKey(FormEntry, models.CASCADE)
    field = models.ForeignKey(FormField, models.CASCADE)
    value = models.TextField(_("value"), blank=True)
