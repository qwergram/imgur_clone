from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import ImagerProfile
from .forms import EditProfile
from imager_images.models import Photo, PUBLIC

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        try:
            photo = Photo.objects.filter(published=PUBLIC).order_by("?")[0]
        except IndexError:
            photo = None

        return {
            "random_photo": photo
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
            return HttpResponse("POST method!")

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
