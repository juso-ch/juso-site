from content_editor.admin import ContentEditorInline
from juso.testimonials.models import Campaign
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


class TestimonialPlugin(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        models.CASCADE,
        verbose_name=_("campaign"),
        related_name="%(app_label)s_%(class)s",
    )

    title = models.CharField(max_length=255, blank=True)
    count = models.IntegerField(default=3)
    css_class = models.CharField(max_length=30, blank=True)
    create_url = models.CharField(max_length=280, blank=True)
    button_text = models.CharField(max_length=280, default="Einreichen")

    class Meta:
        abstract = True


class TestimonialInline(ContentEditorInline):
    autocomplete_fields = ['campaign']


def render_testimonials(plugin):
    campaign = plugin.campaign

    selected = campaign.testimonial_set.filter(
        public=True).order_by('?')[:plugin.count]

    return render_to_string("testimonials/plugin.html", {
        'selected': selected,
        'plugin': plugin,
    })
