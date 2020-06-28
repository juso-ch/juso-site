from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = "juso.blog"
    verbose_name = _("blog")
