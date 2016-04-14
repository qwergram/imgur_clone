from django.shortcuts import render, get_object_or_404, redirect
from .models import Album, Photo, PUBLIC

# Create your views here.

def latest_library_view(request, **kwargs):
    return render(request, "library_view.html", {"photos": Photo.objects.filter(published=PUBLIC).order_by("-date_uploaded")[:100]})

def album_view(request, album_id=None, **kwargs):
    if album_id:
        photos = get_object_or_404(Album, id=album_id).photos.all()
    else:
        return redirect('library')
    return render(request, "library_view.html", {"photos": photos})

def photo_view(request, photo_id=None, **kwrags):
    if photo_id:
        photo = get_object_or_404(Photo, id=photo_id)
    else:
        return redirect('library')
    return render(request, "photo_view.html", {"photo": photo})
