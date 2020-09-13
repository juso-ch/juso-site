import numbers
import hashlib

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from ipaddr import client_ip

from juso.forms import models
from juso.forms.plugins import render_form

# Create your views here.


def form_view(request, pk):
    form = get_object_or_404(models.Form, pk=pk).get_instance(request)

    if request.POST:
        return process_form(request, form)

    return HttpResponse(
        render_to_string("forms/form.html", {"form": form, "disable_js": True,})
    )


def mailtrain_subscribe_url(form):
    return f"{settings.MAILTRAIN_URL}/api/subscribe/{form.list_id}/?access_token={settings.MAILTRAIN_TOKEN}"


def process_form(request, form):
    if form.is_valid():
        # Save entry
        entry = models.FormEntry.objects.create(form=form.form, ip=client_ip(request),)

        for field in form.form.forms_formfield_set.all():
            field_entry = models.FormEntryValue.objects.create(
                field=field, form_entry=entry, value=form.cleaned_data[field.slug],
            )
            if isinstance(form.cleaned_data[field.slug], numbers.Number):
                field_entry.int_value = form.cleaned_data[field.slug]
                field_entry.save()

        data = form.form.webhook_dict.copy() if form.form.webhook_dict else dict()
        data.update(entry.get_values())

        if form.form.webhook:
            requests.post(form.form.webhook, data=data)

        if form.form.list_id:
            requests.post(mailtrain_subscribe_url(form.form), data=data)

        if form.form.mailchimp_connection:
            connection = form.form.mailchimp_connection
            email = data.pop("email", "").lower().encode("utf-8")
            email_hash = hashlib.md5(email).hexdigest()

            mailchimp_data = {
                "email_address": email,
                "status_if_new": "subscribed",
                "status": "subscribed",
                "ip_signup": entry.ip,
                "merge_fields": data,
                "tags": (form.form.slug,),
            }

            headers = {"Content-Type": "application/json"}
            auth = ("key", connection.api_key)

            url = f"https://{connection.api_server}.api.mailchimp.com/3.0/lists/{form.form.mailchimp_list_id}/members/{email_hash}"

            r = requests.put(url, json=mailchimp_data, headers=headers, auth=auth,)
            data['email'] = email.decode()

        if form.form.email:
            message = (
                f"Form: {form.form.title} ({form.form.pk})"
                f"\nEntry-ID: {entry.pk}"
                f"\nCreated: {entry.created}"
                f"\nIP: {entry.ip}"
                "\n--------------------------"
            )
            for field in form.form.get_fields():
                message += f"\n{field}: {data.get(field, '')}"
            message += "\n"
            emails = [email.strip() for email in form.form.email.split(",")]
            send_mail(
                f"Form Entry: {form.form.title}",
                message,
                "form@juso.ch",
                emails,
                False,
            )

        data.update({
            'ip': entry.ip,
            'created': entry.created,
            'sid': entry.submission_id,
        })

        if form.form.success_redirect:
            response = HttpResponse(status=201)
            response["URL"] = form.form.success_redirect.format(**data)
            return response

        if form.form.success_message:
            return HttpResponse(form.form.success_message.format(**data), status=202)

        form = form.form.get_instance(None)

    return HttpResponse(
        render_to_string("forms/form.html", {"form": form, "disable_js": True,})
    )
