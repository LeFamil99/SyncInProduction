from django.shortcuts import render
import requests
import base64
import json
import urllib.request
import wikipediaapi
import math
import re
import lyricsgenius
import time
import random
from login.models import Song, Album, Author, Profile, Fav

# Identifiants pour se connecter à 'API de Spotify
clientId = "5a3ae217ec7044f981b938869c691130"
clientSecret = "efaf289a8333490bb4e335ca85a83347"

def setUp():
    """Génère le token permettant de se connecter à l'API de Spotify

    Returns:
        String: Le token d'accès
    """
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')


    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']
    
    return token


def getAllInfos(id, token): 
    """Génère toutes les infos nécessaires sur une chanson

    Args:
        id (String): ID Spotify de la chanson
        token (_type_): Token d'accès à l'API de Spotify

    Returns:
        dict: Dictionnaire contenant toutes les infos
    """

    # Requête des infos sur la chanson par le biais de l'API Spotify
    searchUrl = f"https://api.spotify.com/v1/tracks/{id}"
    headers = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(url=searchUrl, headers=headers)
    resd = json.dumps(res.json(), indent=2)
    parsed = res.json()

    # Requête des informations sur tous les artistes "featured" dans la chanson
    featArray = []
    for i in range (len(parsed["artists"]) - 1): 
        featArray.append(getArtist(parsed["artists"][i + 1]["id"], token, 0))

    # Formattage de la durée de la chanson
    duration = parsed["duration_ms"] / 1000
    durationO = {
        "minutes": math.floor(duration / 60),
        "seconds": math.floor(duration - math.floor(duration / 60) * 60)
    }

    # Création du dictionnaire contenant toutes les infos sur la chanson
    o = {
        "artist": {
            "main": getArtist(parsed["artists"][0]["id"], token, 0),
            "other": featArray
        },
        "infos": {
            "id": parsed["id"],
            "title": parsed["name"],
            "duration": durationO,
            "spotify": parsed["external_urls"]["spotify"],
            "youtube": getYoutube(parsed["name"] + " " + parsed["artists"][0]["name"]),
            "lyrics": getLyrics(parsed["name"].split("(")[0], parsed["artists"][0]["name"])
        },
        "album": getAlbumInfos(parsed["album"]["id"], token, parsed["id"], parsed["album"]["total_tracks"]),
        "slug": parsed["id"],
    }

    return o

def getAlbumInfos(albumID, token, currentId, total):
    """Génère toutes les infos nécessaires sur un album

    Args:
        albumID (String): ID Spotify de l'album
        token (String): Token d'accès à l'API de Spotify
        currentId (String): ID Spotify de la chanson ayant appelé la fonction

    Returns:
        dict: Dictionnaire contenant toutes les infos
    """
    
    # Requête des infos sur l'album par le biais de l'API Spotify
    searchUrl = f"https://api.spotify.com/v1/albums/{albumID}"
    headers = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(url=searchUrl, headers=headers)
    resd = json.dumps(res.json(), indent=2)
    parsed = res.json()

    # Génère une liste de toutes les chansons de l'album
    songs = []
    songList = parsed["tracks"]["items"].copy()
    addon = 0
    random.shuffle(songList)

    # for i in range(3):
    #     if len(songList) >= i + addon + 1:
    #         print(currentId, songList[i + addon]["id"])
    #         addon += 1 if songList[i + addon]["id"] == currentId else 0
    #         if len(songList) >= i + addon + 1:
    #             featArray = []
    #             for i in range (len(parsed["artists"]) - 1): 
    #                 featArray.append(getArtist(parsed["artists"][i + 1]["id"], token, 1))

    #             songs.append({
    #                 "name": songList[i + addon]["name"],
    #                 "id": songList[i + addon]["id"],
    #             })

    # Création du dictionnaire contenant toutes les infos sur l'album
    o = {
        "id": parsed["id"],
        "image": parsed["images"][1]["url"],
        "name" : parsed["name"],
        "release_date": parsed["release_date"].split("-")[0],
        "spotify": parsed["external_urls"] ["spotify"],
        "others": songs
    }

    return o

def getOnlyImage(albumID, token):
    """Génère l'URL de l'image d'un album

    Args:
        albumID (String): ID Spotify de l'album
        token (String): Token d'accès à l'API de Spotify

    Returns:
        String: URL de l'image
    """
    # Requête des infos sur l'album par le biais de l'API Spotify
    searchUrl = f"https://api.spotify.com/v1/albums/{albumID}"
    headers = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(url=searchUrl, headers=headers)
    resd = json.dumps(res.json(), indent=2)
    parsed = res.json()

    # Génère et retourne l'URL de l'image
    return parsed["images"][1]["url"]

def getArtist(ID, token, type):

    """Génère toutes les infos nécessaires sur un album

    Args:
        ID (String): ID Spotify de l'artiste
        token (String): Token d'accès à l'API de Spotify
        type (Integer): 0 s'il ne faut pas générer la description de l'auteur

    Returns:
        dict: Dictionnaire contenant toutes les infos
    """
    
    # Requête des infos sur l'album par le biais de l'API Spotify
    searchUrl = f"https://api.spotify.com/v1/artists/{ID}"
    headers = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(url=searchUrl, headers=headers)
    resd = json.dumps(res.json(), indent=2)
    parsed = res.json()
    
    # Génère l'URL de l'image de l'artiste, si cette image existe
    image = ""
    if len(parsed["images"]) > 0:
        image = parsed["images"][1]["url"]

    # Création du dictionnaire contenant toutes les infos sur l'artiste
    o = {
        "id": parsed["id"],
        "name": parsed["name"], 
        "image": image,
        "description": getDesc(parsed["name"], type)
    }

    return o

def getLyrics(songName, artist):
    """Génère les paroles d'une chanson à l'aide de l'API Genius

    Args:
        songName (String): Nom de la chanson
        artist (String): Nom de l'artiste

    Returns:
        String: Paroles de la chanson formattées
    """

    # Requête des paroles par le biais de l'API Genius
    key = "Y-RRX84gWlRVqXEc6K_yUQJdzs3gftwzVIPX0LXRFVY4QSprakvrTYUcOR-FvE_kuHSAeJeRwpX1VQsjiw9qBA"
    genius = lyricsgenius.Genius(key)
    song = genius.search_song(songName, artist)
    
    # Génêre et retourne les paroles formattées
    return song.lyrics if not song == None else "Paroles indisponibles"


def getDesc(name, type):
    """Génère une description de 300 caractères sur l'artiste à l'aide de l'API de Wikipédia

    Args:
        name (String): Nom de l'artiste
        type (int): 0 s'il ne faut pas générer le paragraphe, mais seulement l'URL Wikipédia

    Returns:
        _type_: _description_
    """
    # Requête de la description de l'artiste par le biais de l'API Wikipédia
    wiki_wiki = wikipediaapi.Wikipedia('fr')

    # Gémère toutes les possibilités de string pouvant aller à la fin de l'URL Wikipédia, 
    # permettant de trouver la bonne page
    nameF = name.lower().title()
    nameFF = "_".join(nameF.split(" "))
    formattedNames = [nameFF, nameFF + "_(chanteur)", nameFF + "_(chanteuse)", nameFF + "_(groupe)", nameFF + "_(South_Korean_band)", "_".join(name.split(" "))]
    
    # Pour chaque possibilité, teste si la page correspond à la page d'un artiste, et si oui, 
    # cette page est choisie pour générer la description de l'artiste
    for i in range (len(formattedNames)):
        if "Mc" in formattedNames[i]:
            formattedNames[i] = "Mc".join([x.title() for x in formattedNames[i].split("Mc")])
        #print(formattedNames[i])
        page_py=wiki_wiki.page(formattedNames[i])
        if "musi" in page_py.summary[0:10000] or "DJ" in page_py.summary[0:10000] or "rap" in page_py.summary[0:10000] or "chan" in page_py.summary[0:10000] or "auteur" in page_py.summary[0:10000]:
            return {"content": page_py.summary[0:300], "url": "https://fr.wikipedia.org/wiki/" + formattedNames[i], "found": True} if type == 0 else {"content": "", "url": "https://fr.wikipedia.org/wiki/" + formattedNames[i], "found": True}
    
    return {"content": "Page Wikipédia inexistante", "url": "", "found": False}



    

def getYoutube(name): 
    """Génère l'adresse URL de la chanson sur Youtube

    Args:
        name (String): Nom de la chanson concaténé au nom de l'artiste

    Returns:
        String: URL Youtube de la chanson
    """
    # Formatte le nom pour l'insérer dans l'URL de Youtube
    searchWordCleaned = "".join([i for i in name if i.isalpha() or i.isspace()]).replace(' ', '+')

    # Génère l'URL Youtube du premier résultat lorsque le nom est cherché
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(searchWordCleaned))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    return "https://www.youtube.com/watch?v=" + video_ids[0]



def musics (response, music_slug): 
    """Crée la vue pour la page URL de la musique et stocke les infos de la musique dans la db

    Args:
        response (dict): Contient toutes les infos de la page qui appelle la fonction
        music_slug (String): ID Spotify de la chanson

    Returns:
        _type_: Vue de la page
    """
    song = {}
    try:
        # Vérifie si la chanson est déjà dans la db
        song = Song.objects.filter(spotId=music_slug)[0]
    except:

        # Si non, ajoute la chanson à la db
        print("Song not found, creating ...")
        token = setUp()

        objs = getAllInfos(music_slug, token)
        print(objs)

        try:
            # Vérifie si l'artiste principal est déjà dans la db
            artist = Author.objects.filter(spotId=objs["artist"]["main"]["id"])[0]
        except:
            # Si non, ajoute l'artiste à la db
            print("Artist not found, creating ...")
            Author.objects.create(
                spotId=objs["artist"]["main"]["id"], 
                name=objs["artist"]["main"]["name"],
                desc=objs["artist"]["main"]["description"]["content"],
                found=objs["artist"]["main"]["description"]["found"],
                image=objs["artist"]["main"]["image"],
                link=objs["artist"]["main"]["description"]["url"]
            )
            artist = Author.objects.filter(spotId=objs["artist"]["main"]["id"])[0]
        
        feats = []
        for feat in objs["artist"]["other"]:
            try:
                # Vérifie si chacun des artistes "featured" est déjà dans la db
                feats.append(Author.objects.filter(spotId=feat["id"])[0])
            except:
                # Si non, ajoute les artistes "featured" à la db
                print("Feat artist " + str(feat) + " not found, creating ...")
                Author.objects.create(
                    spotId=feat["id"], 
                    name=feat["name"],
                    desc=feat["description"]["content"],
                    found=feat["description"]["found"],
                    image=feat["image"],
                    link=feat["description"]["url"]
                )
            feats.append(Author.objects.filter(spotId=feat["id"])[0])


        try:
            # Vérifie si l'album est déj;a dans la db 
            album = Album.objects.filter(spotId=objs["album"]["id"])[0]
        except:
            # Si non, ajoute l'album à la db
            print("Album not found, creating ...")
            Album.objects.create(
                spotId=objs["album"]["id"], 
                name=objs["album"]["name"],
                image=objs["album"]["image"],
                link=objs["album"]["spotify"],
                dat=objs["album"]["release_date"],
            )
            album = Album.objects.filter(spotId=objs["album"]["id"])[0]

        # Ajoute la chanson à la db
        Song.objects.create(
            spotId=objs["infos"]["id"], 
            title=objs["infos"]["title"],
            durationS=objs["infos"]["duration"]["seconds"],
            durationM=objs["infos"]["duration"]["minutes"],
            lyrics=objs["infos"]["lyrics"],
            spotLink=objs["infos"]["spotify"],
            ytLink=objs["infos"]["youtube"],
            author=artist,
            album=album,
        )
        song = Song.objects.filter(spotId=music_slug)[0]
        song.feats.set(feats)
        song.save()

    # Génère un dictionnaire contenant les infos sur l'utilisateur, si celui-ci est connecté
    try:
        profile = {"prof": Profile.objects.filter(user=response.user)[0], "is_connected": True}
    except:
        profile = {"is_connected": False}

    # Gère la requête HTTP permettant de mettre/retirer la chanson des favoris
    if response.method == "POST":
        data = response.POST
        action = data.get("fav")
        if action == "like":
            try:
                temp = Fav.objects.filter(song=song, user=profile["prof"])[0]
            except:
                Fav.objects.create(
                    song=song,
                    user=profile["prof"]
                )
        if action == "dislike":
            try:
                Fav.objects.filter(song=song, user=profile["prof"])[0].delete()
            except:
                print("Okok")

    # Si un utilisateur est connecté, détermine si la chanson figure parmis ses favoris ou non
    try:
        profile2 = {"prof": Profile.objects.filter(user=response.user)[0], "is_connected": True}
        favs = Fav.objects.filter(user=profile2["prof"])
        isLiked = False
        for fav in favs:
            if fav.song == song:
                isLiked = True
    except:
        isLiked = False

    return render(response, "musics/index.html", {"song": song, "author": song.author, "album": song.album, "profile": profile, "is_liked": isLiked, "alt_songs": song.album.includes.all})