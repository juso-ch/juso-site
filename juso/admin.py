import secrets

from content_editor.admin import ContentEditorInline
from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.translation import gettext_lazy as _

from juso.sections.models import Section


class RegistrationForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    section = forms.ModelChoiceField(Section.objects.all())
    group = forms.ModelChoiceField(Group.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        if self.request.user.is_superuser:
            return

        self.fields["section"].queryset = self.request.user.section_set.all()
        self.fields["group"].queryset = self.request.user.groups.all()


class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields.get("email", None):
            form.base_fields["email"].required = True

        return form

    change_list_template = "admin/user/change_list.html"

    def register_new_user(self, request):
        form = RegistrationForm(request=request)

        if request.POST:
            form = RegistrationForm(request.POST, request=request)
            if form.is_valid():
                first_name = form.cleaned_data["first_name"].replace(" ", "")
                last_name = form.cleaned_data["last_name"].replace(" ", "")
                username = f"{first_name.lower()}.{last_name.lower()}"

                password = secrets.token_urlsafe(16)

                while User.objects.filter(username=username).exists():
                    username = username + secrets.token_urlsafe(1)

                user = User.objects.create_user(
                    username,
                    email=form.cleaned_data["email"],
                    password=password,
                    is_active=True,
                    is_staff=True,
                )

                if form.cleaned_data["group"]:
                    user.groups.add(form.cleaned_data["group"])

                section = form.cleaned_data["section"]
                section.users.add(user)
                section.save()
                user.save()
                message = """Hallo/Bonjour {first_name} {last_name},

Dein Zugang für/Ton access pour [{section.name}]: {username} / {password}

Admin: https://{section.site.host}/admin/

---
{section.name}"""

                send_mail(
                    f"Account [{section.name}]",
                    message.format(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        password=password,
                        section=section,
                    ),
                    "website@juso.ch",
                    [user.email],
                )

                messages.success(request, _(f"Account for {username} created!"))

                return redirect("admin:auth_user_changelist")

        context = dict(
            self.admin_site.each_context(request),
            form=form,
            title=_("Register new user"),
            app_label="auth",
            opts=User._meta,
            model=User,
        )
        return render(request, "admin/register_new_user.html", context)

    def get_urls(self):
        urls = super().get_urls()
        return [
            path(
                "register-new-user/",
                user_passes_test(lambda user: user.is_staff, login_url="/admin/login/")(
                    self.admin_site.admin_view(self.register_new_user)
                ),
                name="auth_User_register_new_user",
            )
        ] + urls


class ButtonInline(ContentEditorInline):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "text",
                    "target",
                    "region",
                    "ordering",
                )
            },
        ),
        (
            _("display"),
            {
                "classes": ("collapse",),
                "fields": ("color", "style", "line_break", "align"),
            },
        ),
    )


class VotingRecommendationInline(ContentEditorInline):
    fields = ("title", "recommendation", "url", "url_text", "region", "ordering")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
