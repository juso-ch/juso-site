from feincms3.renderer import TemplatePluginRenderer

from juso.blog import models as blog
from juso.events import plugins as event_plugins
from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.blog import plugins as article_plugins
from juso.forms import plugins as form_plugins

from juso import renderer as r

renderer = TemplatePluginRenderer()

renderer.register_string_renderer(
    blog.RichText,
    r.render_richtext
)

renderer.register_string_renderer(
    blog.GlossaryRichText,
    r.render_glossarytext
)

renderer.register_string_renderer(
    blog.HTML,
    r.render_html
)

renderer.register_string_renderer(
    blog.External,
    r.render_embed
)

renderer.register_string_renderer(
    blog.Image,
    r.render_image,
)

renderer.register_string_renderer(
    blog.Download,
    download.render_download
)

renderer.register_string_renderer(
    blog.Team,
    people_plugins.render_team
)

renderer.register_string_renderer(
    blog.EventPlugin,
    event_plugins.render_events
)

renderer.register_string_renderer(
    blog.ArticlePlugin,
    article_plugins.render_articles
)

renderer.register_string_renderer(
    blog.Button,
    r.render_block
)

renderer.register_string_renderer(
    blog.FormPlugin,
    form_plugins.render_form,
)
