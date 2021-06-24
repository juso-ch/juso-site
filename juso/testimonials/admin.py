from django.contrib import admin
from django.utils.translation import gettext as _

# Register your models here.
from .models import Campaign, Testimonial


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "is_active", "email_validation"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "is_active",
                    "section",
                    "create_title",
                    "create_text",
                )
            },
        ),
        (
            _("advanced"),
            {
                "classes": ("collapse", ),
                "fields": (
                    "title_label",
                    "email_validation",
                ),
            },
        ),
        (
            _("meta"),
            {
                "classes": ("collapse", ),
                "fields": (
                    "meta_title",
                    "meta_description",
                ),
            },
        ),
    )

    autocomplete_fields = ['section']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(section__in=sections)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = [
        "first_name", "last_name", "email", "created_at", "validated", "public"
    ]

    list_filter = ['validated', 'public', 'campaign']

    autocomplete_fields = ['campaign']

    fields = (
        "first_name",
        "last_name",
        "email",
        "title",
        "image_ppoi",
        "statement",
        "image",
        "validated",
        "public",
        "campaign",
    )

    actions = [
        'publish_testimonials',
        'unpublish_testimonials',
        'validate_testimonials',
        'invalidate_testimonials',
    ]

    def publish_testimonials(self, request, queryset):
        queryset.update(public=True)

    def unpublish_testimonials(self, request, queryset):
        queryset.update(public=False)

    def validate_testimonials(self, request, queryset):
        queryset.update(validated=True)

    def invalidate_testimonials(self, request, queryset):
        queryset.update(validated=False)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        sections = request.user.section_set.all()
        return qs.filter(campaign__section__in=sections)
