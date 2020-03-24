from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from feincms3.apps import reverse_app, apps_urlconf
from feincms3_sites.middleware import current_site, set_current_site

from juso.models import TranslationMixin
from juso.sections.models import Section
# Create your models here.


class Person(models.Model):
    user = models.OneToOneField(
        User, models.SET_NULL, verbose_name=_("user"),
        blank=True, null=True,
    )

    sections = models.ManyToManyField(
        Section, blank=True,
        verbose_name=_("sections")
    )

    image = models.ImageField(
        _("image"), blank=True, null=True,
        upload_to='people/'
    )

    first_name = models.CharField(max_length=100, verbose_name=_("first name"))
    last_name = models.CharField(max_length=100, verbose_name=_("last name"))

    email = models.EmailField(blank=True, verbose_name=_("e-mail"))
    homepage = models.URLField(blank=True, verbose_name=_("homepage"))
    phone = models.CharField(blank=True, max_length=20, verbose_name=_("phone"))

    facebook = models.URLField(blank=True, verbose_name=_("Facebook"))
    twitter = models.URLField(blank=True, verbose_name=_("Twitter"))
    instagram = models.URLField(blank=True, verbose_name=_("Instagram"))

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        site = current_site()
        if self.sections.filter(site=site).exists():
            return reverse_app(
                [f'{site.id}-people'],
                'person-detail',
                kwargs={
                    'pk': self.pk
                }
            )
        with set_current_site(self.sections.first().site):
            return '//' + self.sections.first().site.host + reverse_app(
                [f'{self.sections.first().site.id}-people'],
                'person-detail',
                urlconf=apps_urlconf(),
                kwargs={
                    'pk': self.pk
                }
            )


class Team(TranslationMixin):
    name = models.CharField(max_length=200, verbose_name=_("name"))

    section = models.ForeignKey(
        Section, models.CASCADE,
        verbose_name=_("section")
    )

    members = models.ManyToManyField(
        Person, through="Membership",
        related_name="teams", verbose_name=_("members")
    )

    order = models.IntegerField(verbose_name=_("order"), default=0)

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")
        ordering = ['order']

    def __str__(self):
        return f'{self.name} ({self.section})'

    def get_absolute_url(self):
        site = current_site()
        if self.section.site == site:
            return reverse_app(
                (f'{self.section.site_id}-people',),
                'team-detail',
                kwargs={
                    'pk': self.pk
                }
            )
        with set_current_site(self.section.site):
            return '//' + self.section.site.host + reverse_app(
                [f'{self.section.site.id}-people'],
                'team-detail',
                urlconf=apps_urlconf(),
                kwargs={
                    'pk': self.pk
                }
            )


class Membership(models.Model):
    person = models.ForeignKey(
        Person, models.CASCADE,
        verbose_name=_("person")
    )
    team = models.ForeignKey(Team, models.CASCADE, verbose_name=_("team"))
    title = models.CharField(max_length=100, verbose_name=_("title"))
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('membership')
        verbose_name_plural = _("memberships")

    def __str__(self):
        return f'{self.person}@{self.team}'
