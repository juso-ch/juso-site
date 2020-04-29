from content_editor.admin import ContentEditorInline
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from juso.forms.models import Form


class FormPlugin(models.Model):
    form = models.ForeignKey(
        Form, models.CASCADE,
        verbose_name=_("form"),
        related_name="+",
        related_query_name="+",
    )

    class Meta:
        abstract = True

class FormPluginInline(ContentEditorInline):
    autocomplete_fields = [
        'form'
    ]


def render_form(form_plugin, request=None):
    form = form_plugin.form.get_instance(request)

    form_html = render_to_string('forms/form.html', {
        'form': form
    })

    script = render_to_string('forms/script.html', {
        'form': form
    })

    return f"""
<div class="form-wrapper" id="form-wrapper-{form_plugin.id}">
{form_html}
</div>
{script}
"""
