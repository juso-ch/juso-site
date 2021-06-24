from django import forms
from django.utils.translation import gettext as _

from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        exclude = ["validated", "public", "campaign", "image_ppoi", "secret"]

    def __init__(self, *args, **kwargs):
        self.campaign = kwargs.pop("campaign")
        super().__init__(*args, **kwargs)
        self.fields["title"].label = self.campaign.title_label

    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)

        email = data['email']

        if Testimonial.objects.filter(campaign=self.campaign,
                                      email=email).exists():
            raise forms.ValidationError(_(
                "Testimonial with %(email)s already exists for this campaign."
            ),
                                        params={'email': email})
        return data

    def save(self, *args, **kwargs):
        self.instance.campaign = self.campaign
        super().save(*args, **kwargs)
