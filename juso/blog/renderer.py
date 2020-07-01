from feincms3.renderer import TemplatePluginRenderer

from juso.blog import models as blog
from juso.renderer import register_renderers

renderer = TemplatePluginRenderer()

register_renderers(renderer, blog)
