from feincms3.renderer import RegionRenderer

from juso.blog import models as blog
from juso.renderer import register_renderers

renderer = RegionRenderer()

register_renderers(renderer, blog)
