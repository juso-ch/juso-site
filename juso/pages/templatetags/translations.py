from django.shortcuts import reverse
from django.conf import settings

from django import template
register = template.Library()

@register.simple_tag
def translations(page, obj=None):
    for language,_ in settings.LANGUAGES:
        if language != page.language_code:
            if obj:
                translation = obj.get_translation_for(language)
                if translation:
                    yield (language, translation)
                    continue
            translation = page.get_translation_for(language)
            if translation:
                yield (language, translation)
