from django.utils.html import mark_safe
from feincms3 import plugins
from django.template.loader import render_to_string

from juso.utils import render_embed


def render_richtext(plugin):
    return render_to_string('plugins/text.html', {
        'content': plugins.richtext.render_richtext(plugin)
    })


def render_glossarytext(plugin):
    return render_to_string('plugins/text.html', {
        'content': mark_safe(plugin.glossary_text)
    })


def render_html(plugin):
    return plugins.html.render_html(plugin)


def render_image(plugin, **kwargs):
    return render_to_string('plugins/image.html', {
        'plugin': plugin,
    })

def render_block(plugin, **kwargs):
    return plugin.render_html()
