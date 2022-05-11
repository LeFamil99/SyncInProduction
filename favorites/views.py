from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from login.models import Profile, Fav, Profile

# Create your views here.

def favorites(response):
    try:
        profile = {"prof": Profile.objects.filter(user=response.user)[0], "is_connected": True}
        favs = profile["prof"].likes.all()

    except:
        profile = {"is_connected": False}
        favs = []

    if response.method == "POST":
        data = response.POST
        action = data.get("fav")
        try:
            Fav.objects.filter(song_id=action, user=profile["prof"])[0].delete()
        except:
            print("Okok")

    return render(response, "login/fav_list.html", {"favs": favs, "profile": profile, "is_empty": len(favs) == 0})

# class FavList(ListView):

#     model = Fav
#     context_object_name = 'favs'

# class CreateView(CreateView):
#     model = Fav


    # 25uBGaikHi0DhMiGMfuXYE
    # Painting Pictures
    # Polo G
    # https://i.scdn.co/image/ab67616d00001e02a493e05c99d8ec5e8020ff2b