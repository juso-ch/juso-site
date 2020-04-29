from feincms3.renderer import TemplatePluginRenderer

from juso.blog import plugins as article_plugins
from juso.events import plugins as event_plugins
from juso.forms import plugins as form_plugins
from juso.pages import models as pages
from juso.people import plugins as people_plugins
from juso.plugins import download

from juso import renderer as r

renderer = TemplatePluginRenderer()

renderer.register_string_renderer(
    pages.RichText,
    r.render_richtext
)

renderer.register_string_renderer(
    pages.GlossaryRichText,
    r.render_glossarytext
)

renderer.register_string_renderer(
    pages.HTML,
    r.render_html
)

renderer.register_string_renderer(
    pages.External,
    r.render_embed
)

renderer.register_string_renderer(
    pages.Image,
    r.render_image,
)

renderer.register_string_renderer(
    pages.Download,
    download.render_download
)

renderer.register_string_renderer(
    pages.Team,
    people_plugins.render_team
)

renderer.register_string_renderer(
    pages.EventPlugin,
    event_plugins.render_events
)

renderer.register_string_renderer(
    pages.ArticlePlugin,
    article_plugins.render_articles
)

renderer.register_string_renderer(
    pages.Button,
    r.render_block
)

renderer.register_string_renderer(
    pages.FormPlugin,
    form_plugins.render_form,
)
