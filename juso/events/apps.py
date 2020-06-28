from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = "juso.events"
    verbose_name = _("events")
