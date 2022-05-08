from django.shortcuts import render
from django.views.generic.list import ListView
from login.models import Fav 

# Create your views here.

class FavList(ListView):

    model = Fav
    context_object_name = 'favs'

    # 25uBGaikHi0DhMiGMfuXYE
    # Painting Pictures
    # Polo G
    # https://i.scdn.co/image/ab67616d00001e02a493e05c99d8ec5e8020ff2b