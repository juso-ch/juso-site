from content_editor.admin import ContentEditorInline
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from fontawesome_5.fields import IconField

# Create your models here.


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

        super(models.CharField, self).__init__(*args, **kwargs)


class SizeField(models.CharField):

    choices = (
        ('tiny', _("tiny")),
        ('small', _("small")),
        ('medium', _("medium")),
        ('large', _("large")),
        ('big', _("big")),
        ('huge', _("huge")),
        ('massive', _("massive")),
    )

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        kwargs['choices'] = self.choices
        kwargs['blank'] = True

        super(models.CharField, self).__init__(*args, **kwargs)


class SemanticBase(models.Model):
    text = models.CharField(_('text'), max_length=240, blank=True)
    inverted = models.BooleanField(_("inverted"), default=False)

    color = ColorField()
    size = SizeField()

    class Meta:
        abstract = True


class IconBase(SemanticBase):
    icon = IconField()

    class Meta:
        abstract = True


class Button(IconBase):

    style = models.CharField(_("style"), max_length=20, choices=(
        ('', _("none")),
        ('basic', _("basic")),
        ('primary', _("primary")),
        ('tertiary', _("tertiary"))
    ), default='', blank=True)

    target = models.CharField(_("target"), max_length=800)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.text}'


class ButtonInline(ContentEditorInline):
    fieldsets = (
        (None, {
            'fields': (
                ('text', 'target',),
                'region',
                'ordering',
            )
        }),
        (_("display"), {
            'classes': ('collapse',),
            'fields': (
                'color',
                'size',
                'style',
            )
        }),
    )


def render_button(plugin, **kwargs):
    return render_to_string('plugins/button.html', {
        "button": plugin
    })


class Divider(IconBase):
    alignment = models.CharField(
        _("alignment"), max_length=30, blank=True,
        choices=(
            ('left aligned', _("left aligned")),
            ('right aligned', _("right aligned"))
        )
    )

    hidden = models.BooleanField(_("hidden"), default=False)
    section = models.BooleanField(_("section"), default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text or '-'


class DividerInline(ContentEditorInline):
    fieldsets = (
        (None, {
            'fields': (
                'text',
                'region',
                'ordering',
            )
        }),
        (_("display"), {
            'classes': ('collapse',),
            'fields': (
                'color',
                'hidden',
                'section',
            )
        }),
    )


def render_divider(plugin, **kwargs):
    return render_to_string('plugins/divider.html', {
        'divider': plugin
    })


class Header(SemanticBase):
    level = models.SmallIntegerField(_("level"), choices=(
        (i, f'h{i}') for i in range(1, 6)
    ))
    block = models.BooleanField(_("block"))
    dividing = models.BooleanField(_("dividing"))

    class Meta:
        abstract = True


class HeaderInline(ContentEditorInline):
    fieldsets = (
        (None, {
            'fields': (
                'text',
                'level',
                'region',
                'ordering',
            )
        }),
        (_("display"), {
            'classes': ('collapse',),
            'fields': (
                'color',
                'dividing',
                'block',
            )
        }),
    )


def render_header(plugin, **kwargs):
    return render_to_string('plugins/header.html', {
        'header': plugin
    })


def render_image(plugin, **kwargs):
    return render_to_string('plugins/image.html', {
        'plugin': plugin,
    })
