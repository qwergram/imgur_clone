from django import forms


class EditProfile(forms.Form):
    camera = forms.CharField(max_length=255)
    personality_type = forms.CharField(max_length=4)
    category = forms.CharField(max_length=255)
    github = forms.URLField()
    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=False)
    # following = forms.MultipleChoiceField(choices=zip(profile.objects.all(), profile.objects.all()))
