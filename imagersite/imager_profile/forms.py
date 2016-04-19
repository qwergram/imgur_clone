from django import forms
from .models import ImagerProfile as profile

class EditProfile(forms.Form):

    camera = forms.CharField(max_length=255)
    personality_type = forms.CharField(max_length=4)
    category = forms.CharField(max_length=255)
    github = forms.URLField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    # following = forms.MultipleChoiceField(choices=zip(profile.objects.all(), profile.objects.all()))
