from django.shortcuts import render
from django.http import HttpResponse
from login.models import Profile, Song

# Create your views here.

def index(response):
    length = len(Song.objects.all())


    # Retourn la vue de la page d'accueil
    return render(response, "main/index.html", {"length": length})
