# coding=utf-8
"""imagersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from imagersite import settings
from django.conf.urls.static import static

from imager_profile.views import IndexView, profile_view, profile_edit
from imager_images.views import (
    latest_library_view,
    album_view,
    photo_view,
    album_create,
    photo_create,
    photo_edit,
    album_edit,
)


image_patterns = [
    url(r'^images/library/$', latest_library_view, name="library"),
    url(r'^images/albums/(?P<album_id>\d+)/$', album_view, name="albums"),
    url(r'^images/photos/(?P<photo_id>\d+)/$', photo_view, name="photos_view"),
    url(r'^images/albums/add/$', album_create, name="album_create"),
    url(r'^images/photos/add/$', photo_create, name="photo_create"),
    url(r'^images/photos/(?P<photo_id>\d+)/edit/', photo_edit, name="photo_edit"),
    url(r'^images/photos/(?P<album_id>\d+)/edit/', album_edit, name="album_edit"),
]

hmac_patterns = [
    url(r'^accounts/', include('registration.backends.hmac.urls'))
]

profile_patterns = [
    url(r'^$', IndexView.as_view(), name='homepage'),
    url(r'^profile/(?:(?P<profile_id>\d+)/)?$', profile_view, name='profile'),
    url(r'^profile/edit/$', profile_edit, name='profile_edit')
]

admin_patterns = [
    url(r'^admin/', admin.site.urls),
]


urlpatterns = profile_patterns + admin_patterns + hmac_patterns + image_patterns


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
