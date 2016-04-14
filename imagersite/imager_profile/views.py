from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import ImagerProfile
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
