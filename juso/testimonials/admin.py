from django.contrib import admin
from django.utils.translation import gettext as _

# Register your models here.
from .models import Campaign, Testimonial


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "is_active", "email_validation"]
    fieldsets = (
        (None, {"fields": ("name", "description", "is_active",)}),
        (
            _("advanced"),
            {
                "classes": ("collapse",),
                "fields": ("template_name", "title_label", "email_validation",),
            },
        ),
        (
            _("meta"),
            {"classes": ("collapse",), "fields": ("meta_title", "meta_description",)},
        ),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "created_at", "validated", "public"]

    fields = (
        "first_name",
        "last_name",
        "image_ppoi",
        "title",
        "statement",
        "image",
        "validated",
        "public",
        "campaign",
    )
