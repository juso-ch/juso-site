import hashlib

import requests
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from juso.forms import models


def mailtrain_subscribe_url(form):
    return f"{settings.MAILTRAIN_URL}/api/subscribe/{form.list_id}/?access_token={settings.MAILTRAIN_TOKEN}"


@shared_task
def process_entry(pk):
    entry = models.FormEntry.objects.get(pk=pk)
    form = entry.form

    data = form.webhook_dict.copy() if form.webhook_dict else dict()
    data.update(entry.get_values(form.get_fields(), json_safe=True))

    if form.webhook:
        requests.post(form.webhook, data=data)

    if form.list_id:
        requests.post(mailtrain_subscribe_url(form), data=data)

    if form.mailchimp_connection:
        connection = form.mailchimp_connection
        email = data.pop("email", "").lower().encode("utf-8")
        email_hash = hashlib.md5(email).hexdigest()

        mailchimp_data = {
            "email_address": email,
            "status_if_new": "subscribed",
            "status": "subscribed",
            "ip_signup": entry.ip,
            "merge_fields": data,
            "tags": [x.strip() for x in form.tags.split(",")],
        }

        headers = {"Content-Type": "application/json"}
        auth = ("key", connection.api_key)

        url = f"https://{connection.api_server}.api.mailchimp.com/3.0/lists/{form.mailchimp_list_id}/members/{email_hash}"

        requests.put(
            url,
            json=mailchimp_data,
            headers=headers,
            auth=auth,
        )
        data["email"] = email.decode()

    if form.email:
        message = (
            f"Form: {form.title} ({form.pk})"
            f"\nEntry-ID: {entry.pk}"
            f"\nCreated: {entry.created}"
            f"\nIP: {entry.ip}"
            "\n--------------------------"
        )
        for field in form.get_fields():
            message += f"\n{field}: {data.get(field, '')}"
        message += "\n"
        emails = [email.strip() for email in form.email.split(",")]
        send_mail(
            f"Form Entry: {form.title}",
            message,
            "form@juso.ch",
            emails,
            False,
        )
