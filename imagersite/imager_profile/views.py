from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import ImagerProfile
from .forms import EditProfile
from imager_images.models import Photo, PUBLIC

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        return {
            "photos": Photo.objects.filter(published=PUBLIC).order_by("?")[:100]
        }


def profile_view(request, profile_id=None, **kwargs):
    if not profile_id:
        profile = request.user.profile
    else:
        profile = get_object_or_404(ImagerProfile, id=int(profile_id))

    return render(request, "profile.html", context={"profile": profile})


def profile_edit(request, *args, **kwargs):
    profile = request.user.profile
    if request.method == "POST":
        form = EditProfile(request.POST)
        if form.is_valid():
            profile.camera = form.cleaned_data.get('camera')
            profile.personality_type = form.cleaned_data.get('personality_type')
            profile.category = form.cleaned_data.get('category')
            profile.github = form.cleaned_data.get('github')
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            if form.cleaned_data.get('password') and form.cleaned_data.get('password') == form.cleaned_data.get('password_confirm'):
                profile.user.set_password(form.cleaned_data.get('password'))
            profile.save()
            profile.user.save()
            return redirect('profile')

        return HttpResponse("Invalid!")
    else:
        return render(request, "edit_profile.html", {"form": EditProfile(initial={
            "camera": profile.camera,
            "personality_type": profile.personality_type,
            "category": profile.category,
            "github": profile.github,
            "first_name": profile.user.first_name,
            "last_name": profile.user.last_name,
            "email": profile.user.email,
        })})
