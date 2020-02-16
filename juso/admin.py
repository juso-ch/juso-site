from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields.get('email', None):
            form.base_fields['email'].required = True

        return form


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
