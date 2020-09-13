from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from feincms3.mixins import LanguageMixin


class TranslationMixin(LanguageMixin):
    translations = models.ManyToManyField(
        "self", related_name=_("translations"), blank=True
    )

    def get_translation_for(self, language_code):
        qs = self.translations.filter(language_code=language_code)
        if qs.exists():
            return qs[0]

    class Meta:
        abstract = True


class ColorField(models.CharField):
    choices = (
        ("red", _("red")),
        ("orange", _("orange")),
        ("yellow", _("yellow")),
        ("olive", _("olive")),
        ("blue", _("blue")),
        ("green", _("green")),
        ("teal", _("teal")),
        ("violett", _("violett")),
        ("purple", _("purple")),
        ("pink", _("pink")),
        ("brown", _("brown")),
        ("grey", _("grey")),
        ("black", _("black")),
    )

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 20
        kwargs["choices"] = self.choices
        kwargs["blank"] = True

        super().__init__(*args, **kwargs)


class AbstractBlock(models.Model):
    text = models.CharField(_("text"), max_length=240, blank=True,)

    color = ColorField()

    class Meta:
        abstract = True

    def render_html(self):
        raise NotImplementedError


class Button(AbstractBlock):

    style = models.CharField(
        _("style"),
        max_length=20,
        choices=(("", _("none")), ("secondary", _("secondary"))),
        default="",
        blank=True,
    )

    align = models.CharField(
        _("alignment"),
        max_length=30,
        blank=True,
        choices=(
            ("", _("default")),
            ("center", _("center")),
            ("right", _("right")),
            ("block", _("block")),
        ),
    )

    line_break = models.BooleanField(_("break"), default=True)

    target = models.CharField(_("target"), max_length=800)

    class Meta:
        abstract = True

    def render_html(self):
        return render_to_string("button.html", {"button": self})

    def __str__(self):
        return f"{self.text}"


class VotingRecommendation(models.Model):
    title = models.CharField(max_length=300, verbose_name=_("title"))
    url = models.URLField(verbose_name=_("url"))
    url_text = models.CharField(max_length=130, verbose_name=_("link text"))

    recommendation = models.CharField(
        max_length=10,
        choices=(("yes", _("yes")), ("no", _("no")), ("open", _("open")),),
    )

    class Meta:
        abstract = True
        verbose_name = _("voting recommendation")
        verbose_name_plural = _("voting recommendations")

    def __str__(self):
        return self.title
