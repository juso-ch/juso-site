from feincms3.renderer import TemplatePluginRenderer

from juso.events import models as events
from juso.renderer import register_renderers, render_image

renderer = TemplatePluginRenderer()
register_renderers(renderer, events)

location_renderer = TemplatePluginRenderer()

location_renderer.register_string_renderer(
    events.LocationImage,
    render_image
)
