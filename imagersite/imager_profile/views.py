from django.shortcuts import render
from django.views.generic import TemplateView
from imager_images.models import Photo

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        return {
            random_photo: Photo.objects.filter(published=Photo.PUBLIC).order_by("-date_uploaded")[:100].order_by("?")[0]
        }
