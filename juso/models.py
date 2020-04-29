from django.db import models
from django.utils.translation import gettext as _
from feincms3.mixins import LanguageMixin
from django.template.loader import render_to_string


class TranslationMixin(LanguageMixin):
    translations = models.ManyToManyField(
        "self", related_name=_("translations"),
        blank=True
    )

    class Meta:
        abstract = True


class ColorField(models.CharField):
    choices = (
        ('red', _("red")),
        ('orange', _("orange")),
        ('yellow', _("yellow")),
        ('olive', _("olive")),
        ('green', _("green")),
        ('teal', _("teal")),
        ('violett', _("violett")),
        ('purple', _("purple")),
        ('pink', _("pink")),
        ('brown', _("brown")),
        ('grey', _("grey")),
        ('black', _("black")),
    )

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        kwargs['choices'] = self.choices
        kwargs['blank'] = True

        super().__init__(*args, **kwargs)


class AbstractBlock(models.Model):
    text = models.CharField(
        _("text"), max_length=240, blank=True,
    )

    color = ColorField()

    class Meta:
        abstract = True

    def render_html(self):
        raise NotImplementedError


class Button(AbstractBlock):

    style = models.CharField(_("style"), max_length=20, choices=(
        ('', _("none")),
        ('secondary', _("secondary"))
    ), default='', blank=True)

    target = models.CharField(_("target"), max_length=800)

    class Meta:
        abstract = True

    def render_html(self):
        return render_to_string(
            'button.html', {
                'button': self
            }
        )

    def __str__(self):
        return f'{self.text}'
