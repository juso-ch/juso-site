from feincms3.renderer import TemplatePluginRenderer

from juso.pages import models as pages
from juso.renderer import register_renderers

renderer = TemplatePluginRenderer()
register_renderers(renderer, pages)
