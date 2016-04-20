# coding=utf-8
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.http import HttpResponse
from .models import Album, Photo, PUBLIC, PRIVATE
from .forms import NewImage, NewAlbum, EditPhoto
from itertools import chain

def latest_library_view(request, **kwargs):
    return render(
        request,
        "library_view.html",
        {"photos":
            list(chain(
                Album.objects.filter(published=PUBLIC).order_by("-date_uploaded")[:100],
                Photo.objects.filter(published=PUBLIC).order_by("-date_uploaded")[:100]
            ))
        }
    )


def album_view(request, album_id=None, **kwargs):
    album = get_object_or_404(Album, id=int(album_id))
    if album.published == PRIVATE and album.owner.user != request.user:
        raise Http404
    return render(request, "library_view.html", {"photos": album.photos.all()})


def photo_view(request, photo_id=None, **kwargs):
    photo = get_object_or_404(Photo, id=int(photo_id))
    if photo.published == PRIVATE and photo.owner.user != request.user:
        raise Http404
    return render(request, "photo_view.html", {"photo": photo})


def album_create(request, **kwargs):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return redirect('auth_login')

        form = NewAlbum(request.POST, profile_=request.user.profile)
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
                {'form': form, 'what': 'album'}
            )
    else:
        print(Photo.objects.filter(owner__id=request.user.profile.id))
        form = NewAlbum(profile_=request.user.profile)
        return render(
            request,
            "photo_upload.html",
            {"form": form, "what": "album"}
        )


def photo_create(request, **kwargs):
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
            return redirect('photos_view', photo_id=photo.id)
        return HttpResponse('Upload failed!')
    else:
        return render(
            request,
            "photo_upload.html",
            {"form": NewImage(), "what": "photo"}
        )


def photo_edit(request, photo_id, **kwargs):
    if request.method == "POST":
        form = EditPhoto(request.POST, request.FILES)
        photo = get_object_or_404(Photo, id=photo_id)
        if form.is_valid() and request.user.profile.id == photo.owner.id:
            import pdb; pdb.set_trace()
            photo.title = form.cleaned_data.get('title')
            photo.description = form.cleaned_data.get('description')
            photo.published = form.cleaned_data.get('published')
            if form.cleaned_data.get('photo'):
                photo.photo = form.cleaned_data.get('photo')
            photo.save()
            return redirect("photos_view", photo_id=photo.id)
    else:
        photo = get_object_or_404(Photo, id=photo_id)
        return render(
            request,
            "photo_upload.html",
            {"form": EditPhoto(initial={
                "title": photo.title,
                "description": photo.description,
                "published": photo.published,
                "photo": photo.photo,
            }), "what": "photo"}
        )
