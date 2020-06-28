from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from content_editor.admin import ContentEditorInline


class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields.get("email", None):
            form.base_fields["email"].required = True

        return form


class ButtonInline(ContentEditorInline):
    fieldsets = (
        (None, {"fields": (("text", "target"), "region", "ordering",)}),
        (
            _("display"),
            {
                "classes": ("collapse",),
                "fields": ("color", "style", "line_break", "align"),
            },
        ),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
