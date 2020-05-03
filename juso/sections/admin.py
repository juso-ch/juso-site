from django.contrib import admin
from django.utils.translation import gettext as _
from feincms3.admin import TreeAdmin

from juso.sections.models import Category, Section

# Register your models here.


@admin.register(Section)
class SectionAdmin(TreeAdmin):
    list_display = [
        "indented_title",
        "move_column",
        "name",
    ]

    autocomplete_fields = [
        'users',
        'site',
        'parent'
    ]

    prepopulated_fields = {
        'slug': ('name',),
    }

    fieldsets = (
        (None, {
            'fields': ('name', 'users', 'parent')
        }),
        (_("advanced"), {
            'classes': ('collapse',),
            'fields': ('slug', 'site')
        })
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(pk__in=sections)

    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    list_display = [
        "indented_title",
        "move_column",
        'name', 'slug', 'parent', 'language_code'
    ]
    list_filter = ['language_code']
    search_fields = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}

    autocomplete_fields = [
        'parent', 'translations'
    ]

    fieldsets = (
        (None, {
            "fields": (
                'name', 'slug',
                'language_code',
                'parent',
                'header_image',
                'header_image_ppoi',
                'color',
            )
        }),
        (_("translations"), {
            'classes': ('collapse',),
            'fields': ('translations',),
        })
    )
