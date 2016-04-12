from django.shortcuts import render

# Create your views here.

def index_view(request, *args, **kwargs):
    return render(request, template_name="index.html", context={})
