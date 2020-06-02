from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.db import models
from juso.pages.models import Page

# Create your models here.


class Subscription(models.Model):
    page = models.ForeignKey(
        Page, models.CASCADE,
        verbose_name=_('page'),
    )
    subscription_info = JSONField()

    def endpoint(self):
        return self.subscription_info['endpoint']