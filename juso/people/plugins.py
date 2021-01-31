from content_editor.admin import ContentEditorInline
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from juso.people.models import CandidateList, Team


class TeamPlugin(models.Model):
    team = models.ForeignKey(Team,
                             models.CASCADE,
                             verbose_name=_("team"),
                             related_name="+")

    template_key = models.CharField(
        max_length=100,
        default="teams/default.html",
        choices=settings.TEAM_TEMPLATE_CHOICES,
    )

    class Meta:
        abstract = True
        verbose_name = "team"
        verbose_name_plural = "teams"

    def __str__(self):
        return self.team.name


class TeamPluginInline(ContentEditorInline):
    autocomplete_fields = [
        "team",
    ]


def render_team(plugin, **kwargs):
    return render_to_string(
        plugin.template_key,
        {
            "team": plugin.team,
            "plugin": plugin,
        },
    )


class CandidatePlugin(models.Model):
    candidate_list = models.ForeignKey(
        CandidateList,
        models.CASCADE,
        verbose_name=_("candidate_list"),
        related_name="+",
    )

    class Meta:
        abstract = True
        verbose_name = "candidate list"
        verbose_name_plural = "candidate lists"

    def __str__(self):
        return self.candidate_list.name


class CandidateListPluginInline(ContentEditorInline):
    autocomplete_fields = [
        "candidate_list",
    ]


def render_candidate_list(plugin, **kwargs):
    return render_to_string(
        "teams/candidate_list.html",
        {
            "candidate_list": plugin.candidate_list,
            "plugin": plugin,
        },
    )
