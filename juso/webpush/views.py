import json

from django.http import JsonResponse
from feincms3.apps import page_for_app_request

from juso.webpush.models import Subscription


# Create your views here.
def subscribe_to_webpush(request):
    data = json.loads(request.body)
    page = page_for_app_request(request)
    if Subscription.objects.filter(
            page=page, subscription_info__endpoint=data["endpoint"]).exists():
        return JsonResponse({"subscribed": False})

    Subscription.objects.create(page=page, subscription_info=data)

    return JsonResponse({"subscribed": True})


def is_subscribed(request):
    data = json.loads(request.body)
    return JsonResponse({
        "subscribed":
        Subscription.objects.filter(
            page=page_for_app_request(request),
            subscription_info__endpoint=data["endpoint"],
        ).exists()
    })


def unsubscribe_from_webpush(request):
    data = json.loads(request.body)
    page = page_for_app_request(request)
    Subscription.objects.filter(
        page=page, subscription_info__endpoint=data["endpoint"]).delete()

    return JsonResponse({"unsubscribed": True})
