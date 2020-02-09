from feincms3.renderer import TemplatePluginRenderer
from feincms3 import plugins

from juso.blog import models as blog


renderer = TemplatePluginRenderer()

renderer.register_string_renderer(
    blog.RichText,
    lambda plugin: plugins.richtext.render_richtext(plugin)
)

renderer.register_string_renderer(
    blog.HTML,
    lambda plugin: plugins.html.render_html(plugin)
)

renderer.register_string_renderer(
    blog.External,
    lambda plugin: plugins.external.render_external(plugin)
)

renderer.register_string_renderer(
    blog.Image,
    lambda plugin: plugins.image.render_image(plugin)
)
