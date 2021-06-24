import secrets
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from feincms3.mixins import LanguageMixin
from feincms3_meta.models import MetaMixin
from imagefield.fields import ImageField

from juso.sections.models import Section

# Create your models here.


def generate_secret():
    return secrets.token_urlsafe(40)


class Campaign(LanguageMixin, MetaMixin):
    name = models.CharField(_("name"), max_length=100)

    section = models.ForeignKey(Section, models.CASCADE)

    create_title = models.CharField(verbose_name=_("create title"),
                                    blank=True,
                                    max_length=255)
    create_text = models.TextField(verbose_name=_("create text"), blank=True)

    title_label = models.CharField(_("label for title"), max_length=180)
    email_validation = models.BooleanField(_("enable email validation"))
    is_active = models.BooleanField(_("is active"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("campaign")
        verbose_name_plural = _("campaigns")


class Testimonial(models.Model):
    campaign = models.ForeignKey(Campaign, models.CASCADE)

    first_name = models.CharField(_("first name"), max_length=180)
    last_name = models.CharField(_("last name"), max_length=180)
    email = models.EmailField(_("e-mail"))
    title = models.CharField(_("title"), max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)

    statement = models.TextField(_("statement"), max_length=280)

    image = ImageField(
        _("image"),
        auto_add_fields=True,
        formats={
            "square": ["default", ("crop", (660, 660))],
        },
    )

    validated = models.BooleanField(_("validate"), default=False)
    public = models.BooleanField(_("public"), default=False)

    secret = models.CharField(
        verbose_name=_("secret"),
        max_length=280,
        default=generate_secret,
    )

    def save(self, *args, **kwargs):
        if not self.validated and not self.campaign.email_validation:
            self.validated = True
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("testimonial")
        verbose_name_plural = _("testimonials")
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=['campaign', 'email'],
                name="unique_email_per_campaign",
            )
        ]
