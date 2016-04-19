from django import forms
from .models import PRIVACY_CHOICES


class NewImage(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField()
    published = forms.ChoiceField(choices=PRIVACY_CHOICES)
    photo = forms.ImageField()
