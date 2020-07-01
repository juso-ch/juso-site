from admin_ordering.admin import OrderableAdmin
from django.contrib import admin

from juso.link_collections.models import Collection, Link

# Register your models here.


class LinkInline(OrderableAdmin, admin.TabularInline):
    model = Link
    ordering_field = "order"
    ordering_field_hide_input = True

    fields = ("text", "target", "category", "order")

    autocomplete_fields = ["category"]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name", "section"]
    inlines = [LinkInline]

    list_filter = [
        "section",
    ]

    autocomplete_fields = ["section"]

    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(section__in=request.user.section_set.all())

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        section_field = form.base_fields["section"]
        section_field.required = True

        sections = request.user.section_set.all()
        section_field.initial = sections[0]

        return form
