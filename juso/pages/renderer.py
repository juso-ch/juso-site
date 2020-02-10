from django.utils.html import mark_safe
from feincms3 import plugins
from feincms3.renderer import TemplatePluginRenderer

from juso.pages import models as pages

renderer = TemplatePluginRenderer()

renderer.register_string_renderer(
    pages.RichText,
    lambda plugin: plugins.richtext.render_richtext(plugin)
)

renderer.register_string_renderer(
    pages.HTML,
    lambda plugin: plugins.html.render_html(plugin)
)

renderer.register_string_renderer(
    pages.External,
    lambda plugin: plugins.external.render_external(plugin)
)

renderer.register_string_renderer(
    pages.Image,
    lambda plugin: plugins.image.render_image(plugin)
)
