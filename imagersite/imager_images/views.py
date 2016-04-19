# coding=utf-8
from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponse
from .models import Album, Photo, PUBLIC, PRIVATE, PRIVACY_CHOICES
from .forms import NewImage


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
    if photo.published == PRIVATE and photo.owner.user.id != request.user.id:
        raise Http404
    return render(request, "photo_view.html", {"photo": photo})


def album_create(request, **kwargs):
    raise Http404("wat")
    return render(
        request,
        "photo_upload.html",
        {"form": NewImage()}
    )


def photo_create(request, **kwargs):
    print(request.method)
    if request.method == "POST":
        form = NewImage(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated():
            photo = Photo(
                owner=request.user.profile,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                published=form.cleaned_data.get('published'),
                photo=form.cleaned_data.get('photo'),
            )
            photo.save()
            return HttpResponse('Upload success!')
        return HttpResponse('Upload failed!')
    else:
        return render(
            request,
            "photo_upload.html",
            {"form": NewImage()}
        )
