from django.shortcuts import render

# Create your views here.

def latest_library_view(request, **kwargs):
    return render(request, "library_view.html", {})

def album_view(request, album_id=None, **kwargs):
    pass

def photo_view(request, photo_id=None, **kwrags):
    pass
