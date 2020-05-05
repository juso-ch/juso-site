from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class LinkCollectionsConfig(AppConfig):
    name = 'juso.link_collections'
    verbose_name = _("link collections")
