from feincms3.renderer import RegionRenderer

from juso.events import models as events
from juso.renderer import register_renderers, render_image

renderer = RegionRenderer()
register_renderers(renderer, events)

location_renderer = RegionRenderer()

location_renderer.register_string_renderer(events.LocationImage, render_image)
