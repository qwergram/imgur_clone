from django import forms
from .models import PRIVACY_CHOICES, Photo


class NewImage(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField()
    published = forms.ChoiceField(choices=PRIVACY_CHOICES)
    photo = forms.ImageField()


class NewAlbum(forms.Form):

    def __init__(self, profile, *args, **kwargs):
        super(NewAlbum, self).__init__(*args, **kwargs)
        self.fields['photo'].choices = zip(
                Photo.objects.filter(owner__id=profile.id),
                Photo.objects.filter(owner__id=profile.id))

    title = forms.CharField(max_length=255)
    description = forms.CharField()
    published = forms.ChoiceField(choices=PRIVACY_CHOICES)
    photo = forms.MultipleChoiceField()


class EditPhoto(forms.Form):

    title = forms.CharField(max_length=255)
    description = forms.CharField()
    published = forms.ChoiceField(choices=PRIVACY_CHOICES)
    photo = forms.ImageField(required=False)
