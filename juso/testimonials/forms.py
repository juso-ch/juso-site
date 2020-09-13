from django import forms

from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        exclude = ["validated", "public", "campaign", "image_ppoi"]

    def __init__(self, *args, **kwargs):
        self.campaign = kwargs.pop("campaign")
        super().__init__(*args, **kwargs)
        self.fields["title"].label = self.campaign.title_label

    def save(self, *args, **kwargs):
        self.instance.campaign = self.campaign
        super().save(*args, **kwargs)
