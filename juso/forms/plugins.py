from content_editor.admin import ContentEditorInline
from django.core.validators import int_list_validator
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from juso.forms.models import Form


class FormPlugin(models.Model):
    form = models.ForeignKey(
        Form,
        models.CASCADE,
        verbose_name=_("form"),
        related_name="%(app_label)s_%(class)s",
    )

    class Meta:
        abstract = True


class EntryCounter(models.Model):
    form = models.ForeignKey(
        Form,
        models.CASCADE,
        verbose_name=_("form"),
        related_name="%(app_label)s_%(class)s",
    )

    steps = models.CharField(
        verbose_name=_("steps"),
        max_length=200,
        validators=[int_list_validator()],
        default="50, 100, 500, 1000",
    )

    prefix = models.CharField(max_length=100, blank=True, verbose_name=_("pefix"))
    suffix = models.CharField(max_length=100, blank=True, verbose_name=_("suffix"))

    prefix_missing = models.CharField(
        max_length=100, blank=True, verbose_name=_("pefix missing")
    )
    suffix_missing = models.CharField(
        max_length=100, blank=True, verbose_name=_("suffix missing")
    )
    aggregate_field = models.SlugField(
        _("aggregate field"),
        blank=True,
        help_text=_(
            "use if you don't want the count of entries, but the sum of a field"
        ),
    )

    start = models.IntegerField(_("start"), default=0)

    template_key = models.CharField(
        _("template"),
        choices=(("forms/bar.html", _("bar")), ("forms/number.html", _("number")),),
        default="forms/bar.html",
        max_length=40,
    )

    class Meta:
        abstract = True


class FormPluginInline(ContentEditorInline):
    autocomplete_fields = ["form"]


class EntryCounterInline(ContentEditorInline):
    autocomplete_fields = ["form"]


def render_form(form_plugin, request=None):
    form = form_plugin.form.get_instance(request)

    form_html = render_to_string("forms/form.html", {"form": form})

    script = render_to_string("forms/script.html", {"form": form})

    return f"""
<div class="wrapper" id="form-wrapper-{form_plugin.id}">
{form_html}
</div>
{script}
"""


def render_counter(counter_plugin):
    if counter_plugin.aggregate_field:
        count = counter_plugin.form.aggregate(counter_plugin.aggregate_field)
    else:
        count = counter_plugin.form.count()

    count += counter_plugin.start
    steps = [int(i) for i in counter_plugin.steps.split(",")]

    goal = steps[0]
    i = 0

    while i < len(steps) - 1 and goal < count:
        i += 1
        goal = steps[i]

    percentage = count / goal * 100

    return render_to_string(
        counter_plugin.template_key,
        {
            "count": count,
            "plugin": counter_plugin,
            "goal": goal,
            "percentage": percentage,
            "missing": goal - count,
        },
    )
