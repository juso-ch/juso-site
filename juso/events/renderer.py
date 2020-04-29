from feincms3.renderer import TemplatePluginRenderer

from juso.events import models as events
from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.events import plugins as event_plugins
from juso.blog import plugins as article_plugins
from juso.forms import plugins as form_plugins

from juso import renderer as r

renderer = TemplatePluginRenderer()

renderer.register_string_renderer(
    events.RichText,
    r.render_richtext
)

renderer.register_string_renderer(
    events.HTML,
    r.render_html
)

renderer.register_string_renderer(
    events.External,
    r.render_embed
)

renderer.register_string_renderer(
    events.Image,
    r.render_image,
)

renderer.register_string_renderer(
    events.Download,
    download.render_download
)

renderer.register_string_renderer(
    events.Team,
    people_plugins.render_team
)

renderer.register_string_renderer(
    events.EventPlugin,
    event_plugins.render_events
)

renderer.register_string_renderer(
    events.ArticlePlugin,
    article_plugins.render_articles
)

renderer.register_string_renderer(
    events.Button,
    r.render_block
)

renderer.register_string_renderer(
    events.FormPlugin,
    form_plugins.render_form,
)

location_renderer = TemplatePluginRenderer()

location_renderer.register_string_renderer(
    events.LocationImage,
    r.render_image
)
