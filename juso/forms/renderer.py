from django.template.loader import render_to_string
from feincms3 import plugins
from feincms3.renderer import TemplatePluginRenderer

from juso.forms import models

renderer = TemplatePluginRenderer()


renderer.register_string_renderer(
    models.RichText, lambda plugin: plugins.richtext.render_richtext(plugin)
)


def render_form_field(field):
    return render_to_string(f"forms/fields/{field.input_type}.html", {"field": field,})


renderer.register_string_renderer(
    models.FormField, lambda plugin: render_form_field(plugin)
)
