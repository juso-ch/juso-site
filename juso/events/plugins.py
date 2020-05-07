from content_editor.admin import ContentEditorInline
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _

from juso.models import TranslationMixin
from juso.sections.models import Category, Section
from juso.utils import number_word


class EventPlugin(TranslationMixin):
    events = models.ManyToManyField(
        "events.Event", related_name="+", verbose_name=_("events"), blank=True,
        related_query_name='+',
    )

    count = models.IntegerField(_("count"), default=3)

    @property
    def columns(self):
        if self.events.exists():
            return number_word(min(
                self.events.count(),
                self.count,
            ))
        return number_word(self.count)

    namespace = models.ForeignKey(
        "events.NameSpace", models.SET_NULL, related_name="+",
        verbose_name=_("namespace"), blank=True, null=True,
        related_query_name="+"
    )

    template_key = models.CharField(
        max_length=100, default='events/plugins/default.html',
        choices=settings.EVENT_TEMPLATE_CHOICES,
    )

    category = models.ForeignKey(
        Category, models.SET_NULL, related_name="+",
        verbose_name=_("category"), blank=True, null=True,
        related_query_name="+",
    )

    sections = models.ManyToManyField(
        Section, related_name="+", blank=True,
        related_query_name='+',
    )

    class Meta:
        abstract = True
        verbose_name = _("event plugin")
        verbose_name_plural = _("event plugins")




class EventPluginInline(ContentEditorInline):
    autocomplete_fields = [
        'events', 'category', 'sections',
        'namespace'
    ]

    fieldsets = (
        (None, {
            'fields': (
                'events',
                'language_code',
                'count',
                'category',
                'namespace',
                'sections',
                'template_key',
                'ordering',
                'region'
            )
        }),
    )


def get_event_list(plugin):
    if plugin.events.exists():
        return plugin.events.all()
    from juso.events.models import Event

    events = Event.objects.filter(
        language_code=plugin.language_code,
        end_date__gte=timezone.now()
    )

    if plugin.category:
        events = events.filter(category=plugin.category)

    if plugin.sections.exists():
        events = events.filter(section__in=plugin.sections.all())

    return events[:plugin.count]


def render_events(plugin, **kwargs):
    return render_to_string(
        plugin.template_key, {
            'events': get_event_list(plugin),
            'plugin': plugin,
        }
    )
