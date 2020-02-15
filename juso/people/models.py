from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from feincms3.apps import reverse_app
from feincms3.mixins import LanguageMixin

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

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse_app(
            [f'{section.site_id}-people' for section in self.sections.all()],
            'person-detail',
            kwargs={
                'pk': self.pk
            }
        )


class Team(LanguageMixin):
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
        return reverse_app(
            (f'{self.section.site_id}-people',),
            'team-detail',
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
