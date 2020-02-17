from content_editor.admin import ContentEditor
from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext as _
from js_asset import JS

from feincms3 import plugins

from geopy.geocoders import Nominatim

from juso.people import plugins as people_plugins
from juso.plugins import download
from juso.utils import CopyContentMixin, meta_fieldset
from juso.events import models
from juso.events.models import Location, Event, NameSpace
# Register your models here.


@admin.register(Event)
class EventAdmin(ContentEditor, CopyContentMixin):
    list_display = [
        'title',
        'slug',
        'start_date',
        'end_date',
        'location',
        'category',
        'language_code',
        'namespace',
    ]

    list_filter = [
        'category',
        'language_code',
        'namespace',
        'section',
    ]

    search_fields = [
        'location',
        'title',
        'description',
    ]

    date_hierarchy = 'start_date'

    autocomplete_fields = [
        'category',
        'namespace',
        'author',
        'section',
        'location',
    ]

    search_fields = [
        'title',
        'description',
    ]

    prepopulated_fields = {
        "slug": ("title",),
    }

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'author',
                ('start_date', 'end_date',),
                'location',
                'category',
                'tags',
            )
        }),
        (_('settings'), {
            'classes': ('tabbed',),
            'fields': (
                'language_code',
                'slug',
                'section',
                'namespace',
                'template_key',
            )
        }),
        (_('meta'), {
            'classes': ('tabbed',),
            'fields': (
                'meta_title',
                'meta_author',
                'meta_description',
                'meta_image',
                'meta_image_ppoi',
                'meta_robots',
                'meta_canonical',
            )
        }),
    )

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External),
        download.DownloadInline.create(models.Download),
        people_plugins.TeamPluginInline.create(models.Team),
    ]

    plugins = models.plugins

    actions = ['copy_selected']

    plugins = models.plugins

    class Media:
        js = (
            'admin/js/jquery.init.js',
            JS('https://kit.fontawesome.com/7655daeee1.js', {
                'async': 'async',
                'crossorigin': 'anonymous',
            }, static=False),
            'admin/plugin_buttons.js',
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        section_field = form.base_fields['section']

        sections = request.user.section_set.all()
        section_field.initial = sections[0]

        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(section__in=sections)


@admin.register(Location)
class LocationAdmin(ContentEditor):
    search_fields = [
        'name',
        'street',
        'city',
    ]

    list_display = [
        'name',
        'slug',
        'street',
        'city',
        'lng',
        'lat',
    ]

    list_filter = [
        'city'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    autocomplete_fields = [
        'section'
    ]

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'street',
                ('city', 'zip_code',),
                'country',
            )
        }),
        meta_fieldset,
        (_('advanced'), {
            'classes': ('tabbed',),
            'fields': (
                'section',
                'slug',
                'lat',
                'lng',
            )
        })
    )

    inlines = [
        plugins.image.ImageInline.create(models.LocationImage),
    ]

    def has_change_permission(self, request, obj=None):
        if obj is None or obj.section is None:
            return super().has_change_permission(request, obj)
        sections = request.user.section_set.all()
        return obj.section in sections

    def save_model(self, request, obj, form, change):
        if(not change):
            locator = Nominatim(user_agent=settings.NOMINATIM_USER_AGENT)
            location = locator.geocode(
                f"{obj.street}, {obj.zip_code} {obj.city}, {obj.country}"
            )
            obj.lat = location.latitude
            obj.lng = location.longitude
        super().save_model(request, obj, form, change)


@admin.register(NameSpace)
class NamespaceAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]
