import numbers

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
    return f'{settings.MAILTRAIN_URL}/api/subscribe/{form.list_id}/?access_token={settings.MAILTRAIN_TOKEN}'


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

        if form.form.webhook or form.form.list_id:
            data = form.form.webhook_dict.copy()
            data.update(form.cleaned_data)
            url = form.form.webhook or  mailtrain_subscribe_url(form.form)
            response = requests.post(url, data=data)


        if form.form.email:
            message = (
                f"Form: {form.form.title} ({form.form.pk})"
                f"\nEntry-ID: {entry.pk}"
                f"\nCreated: {entry.created}"
                f"\nIP: {entry.ip}"
                "\n--------------------------"
            )
            for field in form.form.forms_formfield_set.all():
                message += f"\n{field.name}: {form.cleaned_data[field.slug]}"
            message += "\n"
            emails = [email.strip() for email in form.form.email.split(',')]
            send_mail(
                f"Form Entry: {form.form.title}",
                message,
                "form@juso.ch",
                emails,
                False,
            )

        if form.form.success_redirect:
            response = HttpResponse(status=201)
            response["URL"] = form.form.success_redirect
            return response

        if form.form.success_message:
            return HttpResponse(form.form.success_message, status=202)

        form = form.form.get_instance(None)

    return HttpResponse(
        render_to_string("forms/form.html", {"form": form, "disable_js": True,})
    )
