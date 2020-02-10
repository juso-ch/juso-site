from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Person(models.Model):
    user = models.OneToOneField(
        User, models.SET_NULL, verbose_name=_("user"),
        blank=True, null=True,
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    homepage = models.URLField()


class Board(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(
        Person, through="BoardMembership"
    )


class BoardMembership(models.Model):
    person = models.ForeignKey(Person, models.CASCADE)
    board = models.ForeignKey(Board, models.CASCADE)
    description = models.CharField(max_length=100)
