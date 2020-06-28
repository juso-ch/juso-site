from content_editor.admin import ContentEditorInline
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


class Download(models.Model):

    document = models.FileField(verbose_name=_("File"), upload_to="downloads/")

    download_text = models.CharField(max_length=200, verbose_name=_("download text"))

    link_classes = models.CharField(
        max_length=200, blank=True, verbose_name=_("link classes (css)")
    )

    class Meta:
        abstract = True
        verbose_name = _("download")
        verbose_name_plural = _("downloads")

    def __str__(self):
        return self.download_text


class DownloadInline(ContentEditorInline):
    pass


def render_download(plugin, **kwargs):
    return render_to_string("plugins/download.html", {"plugin": plugin})
