from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from pywebpush import webpush, WebPushException

from juso.webpush import models


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_data_to(data, subscription):
    subscription = models.Subscription.objects.get(
        pk=subscription
    )

    try:
        webpush(
            subscription.subscription_info,
            data,
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={
                'sub': f'mailto:{settings.VAPID_EMAIL}'
            }
        )
    except WebPushException as ex:
        subscription.failed_attempts += 1
        subscription.save()
        if subscription.failed_attempts > 5:
            subscription.delete()
        raise ex
