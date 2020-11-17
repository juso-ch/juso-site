from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.utils.translation import ugettext as _
from reversion.admin import VersionAdmin

# Register your models here.
from juso.people.models import (CandidateList, Candidature, Membership, Person,
                                Team)


class TeamInline(admin.TabularInline):
    model = Membership

    autocomplete_fields = ["team", "person"]


class PersonInline(OrderableAdmin, admin.TabularInline):
    model = Membership
    ordering_field = "order"
    ordering_field_hide_input = True

    autocomplete_fields = ["team", "person"]


@admin.register(Person)
class PersonAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "user",
        "email",
    ]

    inlines = [
        TeamInline,
    ]

    autocomplete_fields = [
        "user",
        "sections",
    ]

    search_fields = [
        "first_name",
        "last_name",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": ("first_name", "last_name", "user", "image"),
            },
        ),
        (
            _("social media"),
            {
                "fields": ("facebook", "twitter", "instagram"),
            },
        ),
        (
            _("contact"),
            {
                "fields": ("email", "homepage", "phone"),
            },
        ),
        (
            _("other"),
            {
                "fields": ("job", "birthday", "city", "bio"),
            },
        ),
    )

    list_filter = ["sections", "teams"]

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        if request.user.is_superuser:
            return True
        sections = request.user.section_set.all()
        return obj.sections.filter(pk__in=sections) or obj.sections.count() == 0

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)

        if request.user.is_superuser:
            return True

        sections = request.user.section_set.all()
        return obj.sections.filter(pk__in=sections) or obj.sections.count() == 0


@admin.register(Team)
class TeamAdmin(VersionAdmin, OrderableAdmin, admin.ModelAdmin):
    list_display = [
        "name",
        "section",
        "order",
    ]

    list_editable = ["order"]

    list_filter = [
        "section",
        "language_code",
    ]

    ordering_field = ["order"]
    ordering_field_hide_input = True

    autocomplete_fields = ["section", "translations"]

    inlines = [PersonInline]

    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(section__in=sections)


class CandidateInline(OrderableAdmin, admin.StackedInline):
    model = Candidature
    ordering_field = "order"
    ordering_field_hide_input = True

    autocomplete_fields = ["person"]


@admin.register(CandidateList)
class CandidateListAdmin(admin.ModelAdmin):
    autocomplete_fields = ["sections"]

    list_display = ["name"]

    list_filter = [
        "sections",
    ]

    search_fields = ["name"]

    inlines = [CandidateInline]
