from feincms3 import plugins
from feincms3.renderer import TemplatePluginRenderer

from fomantic_ui import models as fomantic
from juso.utils import render_embed
from juso.plugins import download
from juso.people import plugins as people_plugins
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
    lambda plugin: render_embed(plugin)
)

renderer.register_string_renderer(
    blog.Button,
    lambda plugin: fomantic.render_button(plugin)
)

renderer.register_string_renderer(
    blog.Image,
    lambda plugin: fomantic.render_image(plugin)
)

renderer.register_string_renderer(
    blog.Download,
    lambda plugin: download.render_download(plugin)
)

renderer.register_string_renderer(
    blog.Divider,
    lambda plugin: fomantic.render_divider(plugin)
)

renderer.register_string_renderer(
    blog.Header,
    lambda plugin: fomantic.render_header(plugin)
)

renderer.register_string_renderer(
    blog.Team,
    lambda plugin: people_plugins.render_team(plugin)
)
