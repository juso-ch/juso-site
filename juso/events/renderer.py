from feincms3 import plugins
from feincms3.renderer import TemplatePluginRenderer

from fomantic_ui import models as fomantic
from juso.events import models as events
from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.utils import render_embed

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
    lambda plugin: render_embed(plugin)
)

renderer.register_string_renderer(
    events.Image,
    lambda plugin: fomantic.render_image(plugin)
)

renderer.register_string_renderer(
    events.Download,
    lambda plugin: download.render_download(plugin)
)

renderer.register_string_renderer(
    events.Team,
    lambda plugin: people_plugins.render_team(plugin)
)

renderer.register_string_renderer(
    events.Button,
    lambda plugin: fomantic.render_button(plugin)
)

renderer.register_string_renderer(
    events.Divider,
    lambda plugin: fomantic.render_divider(plugin)
)

renderer.register_string_renderer(
    events.Header,
    lambda plugin: fomantic.render_header(plugin)
)

location_renderer = TemplatePluginRenderer()

location_renderer.register_string_renderer(
    events.LocationImage,
    lambda plugin: fomantic.render_image(plugin)
)
