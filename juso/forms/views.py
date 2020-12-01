import hashlib
import numbers

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from ipaddr import client_ip

from juso.forms import models, tasks
from juso.forms.plugins import render_form

# Create your views here.


@csrf_exempt
def form_view(request, pk):
    form = get_object_or_404(models.Form, pk=pk).get_instance(request)

    if request.POST:
        return process_form(request, form)

    return HttpResponse(
        render_to_string(
            "forms/form.html",
            {
                "form": form,
                "disable_js": True,
            },
        )
    )


def process_form(request, form):
    if form.is_valid():
        # Save entry
        entry = models.FormEntry.objects.create(
            form=form.form,
            ip=client_ip(request),
        )

        for field in form.form.forms_formfield_set.all():
            field_entry = models.FormEntryValue.objects.create(
                field=field,
                form_entry=entry,
                value=form.cleaned_data[field.slug],
            )
            if isinstance(form.cleaned_data[field.slug], numbers.Number):
                field_entry.int_value = form.cleaned_data[field.slug]
                field_entry.save()

        tasks.process_entry.delay(entry.pk)

        data = form.form.webhook_dict.copy() if form.form.webhook_dict else dict()
        data.update(entry.get_values(form.form.get_fields(), json_safe=True))

        data.update(
            {
                "ip": entry.ip,
                "created": entry.created,
                "sid": str(entry.submission_id),
            }
        )

        if form.form.success_redirect:
            response = HttpResponse(status=201)
            response["URL"] = form.form.success_redirect.format(**data)
            return response

        if form.form.success_message:
            message = (
                form.form.success_message.replace("%7B", "{")
                .replace("%7D", "}")
                .format(**data)
                .replace("{", "%7B")
                .replace("}", "%7D")
            )
            return HttpResponse(message, status=202)

        form = form.form.get_instance(None)

    return HttpResponse(
        render_to_string(
            "forms/form.html",
            {
                "form": form,
                "disable_js": True,
            },
        )
    )
