from django.utils.translation import gettext as _
from django.db import models
from django.template.loader import render_to_string
from juso.forms.models import Form
from content_editor.admin import ContentEditorInline


class FormPlugin(models.Model):
    form = models.ForeignKey(
        Form, models.CASCADE,
        verbose_name=_("form")
    )

    class Meta:
        abstract = True

class FormPluginInline(ContentEditorInline):
    pass


def render_form(form_plugin, request=None):
    form = form_plugin.form.get_instance(request)

    return render_to_string(
        'forms/form.html', {
            'form': form
        }
    )
