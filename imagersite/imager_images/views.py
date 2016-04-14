# coding=utf-8
from django.shortcuts import render, get_object_or_404, Http404
from .models import Album, Photo, PUBLIC, PRIVATE


def latest_library_view(request, **kwargs):
    return render(
        request,
        "library_view.html",
        {"photos": Photo.objects.filter(published=PUBLIC).order_by("-date_uploaded")[:100]}
    )


def album_view(request, album_id=None, **kwargs):
    photos = get_object_or_404(Album, id=int(album_id)).photos.all()
    return render(request, "library_view.html", {"photos": photos})


def photo_view(request, photo_id=None, **kwrags):
    photo = get_object_or_404(Photo, id=int(photo_id))
    if photo.published == PRIVATE and photo.owner is not request.user:
        raise Http404
    return render(request, "photo_view.html", {"photo": photo})
