from django import template
from django.conf import settings
from django.shortcuts import reverse

register = template.Library()


@register.simple_tag
def load_translations(page, obj=None):
    return list(list_of_translations(page, obj))


@register.simple_tag
def translations(page, obj=None):
    for language, _ in settings.LANGUAGES:
        if language != page.language_code:
            if obj:
                translation = obj.get_translation_for(language)
                if translation:
                    uri = translation.get_absolute_url()
                    if uri.startswith("//"):
                        uri = scheme + uri
                    else:
                        uri = scheme + "//" + page.site.host + uri
                    yield (language, uri)
                    continue
            translation = page.get_translation_for(language)
            if translation:
                yield (language, translation)


@register.simple_tag
def translation_head(page, obj=None, scheme="https:"):
    if obj:
        yield obj.language_code, scheme + "//" + page.site.host + obj.get_absolute_url()
        for translation in obj.translations.all():
            uri = translation.get_absolute_url()
            if uri.startswith("//"):
                uri = scheme + uri
            else:
                uri = scheme + "//" + page.site.host + uri
            yield translation.language_code, uri
    else:
        yield page.language_code, scheme + "//" + page.site.host + page.path
        for translation in page.translations.all():
            uri = translation.get_absolute_url()
            if uri.startswith("//"):
                uri = scheme + uri
            else:
                uri = scheme + "//" + page.site.host + uri
            yield translation.language_code, uri

def get_uri(obj, page, scheme):
    uri = obj.get_absolute_url()
    if uri.startswith("//"):
        uri = scheme + uri
    else:
        uri = scheme + "//" + page.site.host + uri
    return uri


def list_of_translations(page, obj=None, scheme="https:"):

    if obj:
        yield obj.language_code, scheme + "//" + page.site.host + obj.get_absolute_url()
    else:
        yield page.language_code, scheme + "//" + page.site.host + page.path

    for language, _ in settings.LANGUAGES:
        if language != page.language_code:
            if obj:
                translation = obj.get_translation_for(language)
                if translation:
                    yield (language, get_uri(translation, page, scheme))
                    continue
            translation = page.get_translation_for(language)
            if translation:
                yield (language, get_uri(translation, translation, scheme))
