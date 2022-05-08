from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("<slug:music_slug>", views.musics, name="music"),
]

urlpatterns += staticfiles_urlpatterns()