from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class GlossaryConfig(AppConfig):
    name = 'juso.glossary'
    verbose_name = _("glossary")
