from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = 'juso.pages'
    verbose_name = _("pages")
