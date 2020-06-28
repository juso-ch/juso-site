from django.utils.html import mark_safe
from feincms3 import plugins
from django.template.loader import render_to_string

from juso.blog import plugins as article_plugins
from juso.events import plugins as event_plugins
from juso.forms import plugins as form_plugins
from juso.people import plugins as people_plugins
from juso.plugins import download

from juso.utils import render_embed


def render_richtext(plugin):
    return render_to_string(
        "plugins/text.html", {"content": plugins.richtext.render_richtext(plugin)}
    )


def render_glossarytext(plugin):
    return render_to_string(
        "plugins/text.html", {"content": mark_safe(plugin.glossary_text)}
    )


def render_html(plugin):
    return plugins.html.render_html(plugin)


def render_image(plugin, **kwargs):
    return render_to_string("plugins/image.html", {"plugin": plugin,})


def render_block(plugin, **kwargs):
    return plugin.render_html()


def register_renderers(renderer, pages):
    renderer.register_string_renderer(pages.RichText, render_richtext)

    if hasattr(pages, "GlossaryRichText"):
        renderer.register_string_renderer(pages.GlossaryRichText, render_glossarytext)

    renderer.register_string_renderer(pages.HTML, render_html)

    renderer.register_string_renderer(pages.External, render_embed)

    renderer.register_string_renderer(
        pages.Image, render_image,
    )

    renderer.register_string_renderer(pages.Download, download.render_download)

    renderer.register_string_renderer(pages.Team, people_plugins.render_team)

    renderer.register_string_renderer(pages.EventPlugin, event_plugins.render_events)

    renderer.register_string_renderer(
        pages.ArticlePlugin, article_plugins.render_articles
    )

    renderer.register_string_renderer(pages.Button, render_block)

    renderer.register_string_renderer(
        pages.FormPlugin, form_plugins.render_form,
    )
