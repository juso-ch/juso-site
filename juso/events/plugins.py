from content_editor.admin import ContentEditorInline
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.utils import timezone

from juso.utils import number_word
from juso.models import TranslationMixin

from juso.sections.models import Category, Section
from juso.events.models import Event, NameSpace


class EventPlugin(TranslationMixin):
    events = models.ManyToManyField(
        Event, related_name="+", verbose_name=_("events"), blank=True,
        related_query_name='+',
    )

    count = models.IntegerField(_("count"), default=3)

    @property
    def columns(self):
        return number_word(min(
            self.events.count(),
            self.count,
        ))

    namespace = models.ForeignKey(
        NameSpace, models.SET_NULL, related_name="+",
        verbose_name=_("namespace"), blank=True, null=True,
        related_query_name="+"
    )

    template_key = models.CharField(
        max_length=100, default='events/default.html',
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
