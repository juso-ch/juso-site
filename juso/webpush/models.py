from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from juso.pages.models import Page

# Create your models here.


class Subscription(models.Model):
    page = models.ForeignKey(Page, models.CASCADE, verbose_name=_("page"),)
    subscription_info = JSONField()

    failed_attempts = models.IntegerField(default=0)

    def endpoint(self):
        return self.subscription_info["endpoint"]
