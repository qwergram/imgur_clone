from django.shortcuts import render
from .models import Album, Photo, PUBLIC

# Create your views here.

def latest_library_view(request, **kwargs):
    return render(request, "library_view.html", {"photos": Photo.objects.filter(published=PUBLIC).order_by("-date_uploaded")[:100]})

def album_view(request, album_id=None, **kwargs):
    return render(request, "album_base.html", {})

def photo_view(request, photo_id=None, **kwrags):
    return render(request, "album_base.html", {})
