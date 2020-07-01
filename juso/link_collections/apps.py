from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LinkCollectionsConfig(AppConfig):
    name = "juso.link_collections"
    verbose_name = _("link collections")
