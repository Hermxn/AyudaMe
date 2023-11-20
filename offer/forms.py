from django import forms

from .models import Offer


class OfferCreateForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["price", "comment"]
