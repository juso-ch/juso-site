from feincms3 import plugins
from feincms3.renderer import TemplatePluginRenderer

from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.events import models as events

renderer = TemplatePluginRenderer()

renderer.register_string_renderer(
    events.RichText,
    lambda plugin: plugins.richtext.render_richtext(plugin)
)

renderer.register_string_renderer(
    events.HTML,
    lambda plugin: plugins.html.render_html(plugin)
)

renderer.register_string_renderer(
    events.External,
    lambda plugin: plugins.external.render_external(plugin)
)

renderer.register_string_renderer(
    events.Image,
    lambda plugin: plugins.image.render_image(plugin)
)

renderer.register_string_renderer(
    events.Download,
    lambda plugin: download.render_download(plugin)
)

renderer.register_string_renderer(
    events.Team,
    lambda plugin: people_plugins.render_team(plugin)
)

location_renderer = TemplatePluginRenderer()

location_renderer.register_string_renderer(
    events.LocationImage,
    lambda plugin: plugins.image.render_image(plugin)
)
