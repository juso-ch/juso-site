from django.db import models
from django.utils.translation import gettext as _
from feincms3.mixins import LanguageMixin


class TranslationMixin(LanguageMixin):
    translations = models.ManyToManyField(
        "self", related_name=_("translations"),
        blank=True
    )

    class Meta:
        abstract = True
