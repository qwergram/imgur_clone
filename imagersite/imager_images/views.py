# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.http import HttpResponseForbidden
from .models import Album, Photo, PRIVATE
from .forms import NewImage, NewAlbum, EditPhoto, EditAlbum
from itertools import chain


@login_required
def latest_library_view(request):
    return render(
        request,
        "library_view.html",
        {"photos": list(chain(
            Album.objects.filter(owner=request.user.profile).order_by("-date_uploaded"),
            Photo.objects.filter(owner=request.user.profile).order_by("-date_uploaded")
        ))}
    )


def album_view(request, album_id=None):
    album = get_object_or_404(Album, id=int(album_id))
    if album.published == PRIVATE and album.owner.user != request.user:
        raise Http404
    return render(
        request, "library_view.html",
        {
            "photos": album.photos.all(),
            "album": album
        }
    )


def photo_view(request, photo_id=None):
    photo = get_object_or_404(Photo, id=int(photo_id))
    if photo.published == PRIVATE and photo.owner.user != request.user:
        raise Http404
    return render(request, "photo_view.html", {"photo": photo})


@login_required
def album_create(request):
    if request.method == 'POST':
        form = NewAlbum(request.user.profile, request.POST)
        if form.is_valid():
            album = Album.objects.create(
                owner=request.user.profile,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                published=form.cleaned_data.get('published'),
            )
            album.save()
            album.photos.add(*form.cleaned_data['photos'])
            return redirect('albums', album_id=album.id)
        else:
            return render(
                request,
                "photo_upload.html",
                {'form': form, "what": "a photo", "how": "Create"}
            )
    else:
        print(Photo.objects.filter(owner__id=request.user.profile.id))
        form = NewAlbum(request.user.profile)
        return render(
            request,
            "photo_upload.html",
            {"form": form, "what": "a photo", "how": "Create"}
        )


@login_required
def album_edit(request, album_id):
    if request.method == "POST":
        form = EditAlbum(request.POST, request.FILES)
        album = get_object_or_404(Album, id=album_id)

        if form.is_valid():
            album.title = form.cleaned_data.get('title')
            album.description = form.cleaned_data.get('description')
            album.published = form.cleaned_data.get('published')
            album.save()
            return redirect("album_view", album_id=album.id)
        else:
            return render(
                request,
                "photo_upload.html",
                {"form": form, "what": "an album", "how": "Edit"}
            )
    else:
        album = get_object_or_404(Album, id=album_id)
        if request.user.profile != album.owner:
            # album is not owned by this user
            raise HttpResponseForbidden

        if request.user.profile == album.owner:
            return render(
                request,
                "photo_upload.html",
                {
                    "form": EditAlbum(initial={
                        "title": album.title,
                        "description": album.description,
                        "published": album.published,
                        "photos": album.photos,
                    }),
                    "what": "an album", "how": "Edit"
                }
            )
        else:
            raise HttpResponseForbidden


@login_required
def photo_create(request):
    if request.method == "POST":
        form = NewImage(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(
                owner=request.user.profile,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                published=form.cleaned_data.get('published'),
                photo=form.cleaned_data.get('photo'),
            )
            photo.save()
            return redirect('photos_view', photo_id=photo.id)
        else:
            return render(
                request,
                "photo_upload.html",
                {'form': form, "what": "a photo", "how": "Upload"}
            )
    else:
        return render(
            request,
            "photo_upload.html",
            {"form": NewImage(), "what": "a photo", "how": "Upload"}
        )


@login_required
def photo_edit(request, photo_id):
    if request.method == "POST":
        form = EditPhoto(request.POST, request.FILES)
        photo = get_object_or_404(Photo, id=photo_id)
        if request.user.profile != photo.owner:
            # photo is not owned by this user
            raise HttpResponseForbidden

        if form.is_valid():
            photo.title = form.cleaned_data.get('title')
            photo.description = form.cleaned_data.get('description')
            photo.published = form.cleaned_data.get('published')
            photo.save()
            return redirect("photos_view", photo_id=photo.id)
        else:
            return render(
                request,
                "photo_upload.html",
                {"form": form, "what": "a photo", "how": "Edit"}
            )
    else:
        photo = get_object_or_404(Photo, id=photo_id)
        if request.user.profile == photo.owner:
            return render(
                request,
                "photo_upload.html",
                {
                    "form": EditPhoto(initial={
                        "title": photo.title,
                        "description": photo.description,
                        "published": photo.published,
                        "photo": photo.photo,
                    }),
                    "what": "a photo", "how": "Edit"
                }
            )
        else:
            raise HttpResponseForbidden
