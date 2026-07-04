from feincms3.renderer import RegionRenderer

from juso.pages import models as pages
from juso.renderer import register_renderers

renderer = RegionRenderer()
register_renderers(renderer, pages)
