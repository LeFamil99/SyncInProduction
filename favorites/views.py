from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from login.models import Profile, Fav, Profile


def favorites(response):
    # Ce bloc try tente de trouver les chansons favorites de l'utilisateur connecté. 
    # Le try échoue si aucun utilisateur n'est connecté
    try:
        profile = {"prof": Profile.objects.filter(user=response.user)[0], "is_connected": True}
        favs = profile["prof"].likes.all()

    except:
        profile = {"is_connected": False}
        favs = []

    # La requete HTTP POST permet de supprimer la chanson fasvorite de la db si le X est cliqué
    if response.method == "POST":
        data = response.POST
        action = data.get("fav")
        # Le try s'assure que l'app ne crash pas lors de l'interaction avec la db
        try:
            Fav.objects.filter(song_id=action, user=profile["prof"])[0].delete()
        except:
            print("Okok")

    # Retourne la vue
    return render(response, "login/fav_list.html", {"favs": favs, "profile": profile, "is_empty": len(favs) == 0})
