from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from login.models import Profile 

# Create your views here.

def favorites(response):
    try:
        profile = Profile.objects.filter(user=response.user)[0]
        favs = profile.likes.all()

    except:
        favs = []

    return render(response, "login/fav_list.html", {"favs": favs})

# class FavList(ListView):

#     model = Fav
#     context_object_name = 'favs'

# class CreateView(CreateView):
#     model = Fav


    # 25uBGaikHi0DhMiGMfuXYE
    # Painting Pictures
    # Polo G
    # https://i.scdn.co/image/ab67616d00001e02a493e05c99d8ec5e8020ff2b