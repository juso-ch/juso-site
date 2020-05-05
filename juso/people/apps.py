from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class PeopleConfig(AppConfig):
    name = 'juso.people'
    verbose_name = _("people")
