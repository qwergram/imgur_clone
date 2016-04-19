from django import forms
from .models import ImagerProfile as profile

class EditProfile(forms.Form):

    camera = forms.CharField(max_length=255)
    personality_type = forms.CharField(max_length=4)
    category = forms.CharField(max_length=255)
    github = forms.URLField()
    following = forms.MultipleChoiceField(choices=zip(profile.objects.all(), profile.objects.all()))
