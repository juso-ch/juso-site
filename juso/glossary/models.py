import re

from django.utils.translation import gettext as _
from django.db import models
from feincms3.plugins.richtext import RichText

from juso.models import TranslationMixin

# Create your models here.


def update_glossary(html, entries):
    for entry in entries.all():
        repl = ("<span class=\"glossary\""
                f"data-tooltip=\"{entry.content}\">\g<name></span>"
               )
        html = re.sub(
            entry.pattern,
            repl,
            html, count=2
        )
    return html


class Entry(TranslationMixin):
    name = models.CharField(
        _("name"), max_length=40
    )

    slug = models.SlugField(_("slug"), unique=True)

    auto_pattern = models.BooleanField(
        _("auto-pattern"), default=True
    )

    pattern = models.CharField(_("pattern"), max_length=200, blank=True)
    content = models.TextField(blank=True)


    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.auto_pattern:
            self.pattern = f'(?P<name>{self.name})'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GlossaryContent(RichText):
    entries = models.ManyToManyField(
        Entry, verbose_name=_("entries"),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    glossary_text = models.TextField(blank=True)

    class Meta:
        abstract = True


    def save(self, *args, **kwargs):
        if self.id:
            self.glossary_text = update_glossary(self.text, self.entries)
        else:
            super().save(*args, **kwargs)
            self.glossary_text = update_glossary(self.text, self.entries)
        super().save()

