import re

from django.db import models
from django.utils.translation import gettext_lazy as _
from feincms3.plugins.richtext import RichText

from juso.models import TranslationMixin
from juso.sections.models import Category

# Create your models here.


def update_glossary(html, entries):
    for entry in entries.all():
        repl = (
            f'<label for="gl-{entry.pk}" class="glossary">'
            r"\g<name></label>"
            f'<input type="checkbox" id="gl-{entry.pk}" class="toggle">'
            '<span class="glossary-content">'
            f"<dfn>{entry.name}</dfn>: "
            f"{entry.content}</span>"
        )
        html = re.sub(entry.pattern, repl, html, count=2)
    return html


class Entry(TranslationMixin):
    name = models.CharField(_("name"), max_length=40)

    slug = models.SlugField(_("slug"), unique=True)

    auto_pattern = models.BooleanField(_("auto-pattern"), default=True)

    pattern = models.CharField(_("pattern"), max_length=200, blank=True)
    content = models.TextField(blank=True)
    category = models.ForeignKey(Category, models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if self.auto_pattern:
            self.pattern = f"(?P<name>{self.name})"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GlossaryContent(RichText):
    entries = models.ManyToManyField(
        Entry,
        verbose_name=_("entries"),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    update_glossary = models.BooleanField(default=True)
    glossary_text = models.TextField(blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        print(self.update_glossary)
        if self.update_glossary:
            if self.id:
                self.glossary_text = update_glossary(self.text, self.entries)
            else:
                super().save(*args, **kwargs)
                self.glossary_text = update_glossary(self.text, self.entries)
            self.update_glossary = False
        super().save()
