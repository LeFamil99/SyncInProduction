from django.shortcuts import render
import requests
import base64
import json
import urllib.request
import wikipediaapi
import wikipedia
import math
import re
import lyricsgenius
import time
import random
import array
from login.models import Song, Album, Author, Profile, Fav
#from SpotifySearch import *

# Create your views here.

clientId = "5a3ae217ec7044f981b938869c691130"
clientSecret = "efaf289a8333490bb4e335ca85a83347"

def setUp():
    # Step 1 - Authorization 
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    # Encode as Base64
    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')


    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']
    
    return token


def getID(id, token): 
    tim = time.time()
    
    length = 10

    searchUrl = f"https://api.spotify.com/v1/tracks/{id}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    #print("1 " + str(time.time()-tim))
    tim = time.time()

    resd = json.dumps(res.json(), indent=2)

    #print(resd)
    
    parsed = res.json()

    #print(resd)

    featArray = []
    for i in range (len(parsed["artists"]) - 1): 
        featArray.append(getArtist(parsed["artists"][i + 1]["id"], token, 1))

    #print("2 " + str(time.time()-tim))
    tim = time.time()

    duration = parsed["duration_ms"] / 1000
    durationO = {
        "minutes": math.floor(duration / 60),
        "seconds": math.floor(duration - math.floor(duration / 60) * 60)
    }

    #print("3 " + str(time.time()-tim))
    tim = time.time()
        
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
        "album": getImage(parsed["album"]["id"], token, parsed["id"], parsed["album"]["total_tracks"]),
        "slug": parsed["id"],
    }

    #print("4 " + str(time.time()-tim))
    tim = time.time()
    return o

def getImage(albumID, token, currentId, total):
    
    searchUrl = f"https://api.spotify.com/v1/albums/{albumID}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)

    parsed = res.json()

    songs = []

    songList = parsed["tracks"]["items"].copy()
    addon = 0

    random.shuffle(songList)

    for i in range(3):
        if len(songList) >= i + addon + 1:
            print(currentId, songList[i + addon]["id"])
            addon += 1 if songList[i + addon]["id"] == currentId else 0
            if len(songList) >= i + addon + 1:
                songs.append({
                    "name": songList[i + addon]["name"],
                    "id": songList[i + addon]["id"]
                })

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
    
    searchUrl = f"https://api.spotify.com/v1/albums/{albumID}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)

    #print(resd.split("\"artists\": [")[1])

    parsed = res.json()

    return parsed["images"][1]["url"]

def getArtist(ID, token, type):
    
    searchUrl = f"https://api.spotify.com/v1/artists/{ID}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)

    #print(resd)

    parsed = res.json()
    #print (parsed["images"][1]["url"])
    image = ""

    if len(parsed["images"]) > 0:
        image = parsed["images"][1]["url"]
    o = {
        "id": parsed["id"],
        "name": parsed["name"], 
        "image": image,
        "description": getDesc(parsed["name"], type)
    }

    return o

def getLyrics(songName, artist):
    key = "Y-RRX84gWlRVqXEc6K_yUQJdzs3gftwzVIPX0LXRFVY4QSprakvrTYUcOR-FvE_kuHSAeJeRwpX1VQsjiw9qBA"

    genius = lyricsgenius.Genius(key)

    song = genius.search_song(songName, artist)
    # print(songName, artist)
    # print(song)
    return song.lyrics if not song == None else "Paroles indisponibles"



    # # Encode as Base64
    # message = f"{clientId}:{clientSecret}"
    # messageBytes = message.encode('ascii')
    # base64Bytes = base64.b64encode(messageBytes)
    # base64Message = base64Bytes.decode('ascii')


    # headers['Authorization'] = f"Basic {base64Message}"
    # data['grant_type'] = "client_credentials"

    # r = requests.post(url, headers=headers, data=data)

    # token = r.json()['access_token']
    
    # return token

def getDesc(name, type):
    wiki_wiki = wikipediaapi.Wikipedia('fr')
    nameF = name.lower().title()
    nameFF = "_".join(nameF.split(" "))

    formattedNames = [nameFF, nameFF + "_(chanteur)", nameFF + "_(chanteuse)", "_".join(name.split(" "))]
    #print(formattedNames)
    for i in range (len(formattedNames)):
        if "Mc" in formattedNames[i]:
            formattedNames[i] = "Mc".join([x.title() for x in formattedNames[i].split("Mc")])
        #print(formattedNames[i])
        page_py=wiki_wiki.page(formattedNames[i])
        if "musi" in page_py.summary[0:10000] or "DJ" in page_py.summary[0:10000] or "rap" in page_py.summary[0:10000] or "chan" in page_py.summary[0:10000] or "auteur" in page_py.summary[0:10000]:
            return {"content": page_py.summary[0:300], "url": "https://fr.wikipedia.org/wiki/" + formattedNames[i], "found": True} if type == 0 else {"content": "", "url": "https://fr.wikipedia.org/wiki/" + formattedNames[i], "found": True}
    
    return {"content": "Page Wikipédia inexistante", "url": "", "found": False}

    
    #print("https://fr.wikipedia.org/wiki/" + "_".join(name.split(" ")))

    

def getYoutube(name): 
    searchWordCleaned = "".join([i for i in name if i.isalpha() or i.isspace()]).replace(' ', '+')
    #print(searchWordCleaned)

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(searchWordCleaned))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]


# def getID(query, token): 
    
#     length = 10

#     searchUrl = f"https://api.spotify.com/v1/tracks/{id}"
#     headers = {
#         "Authorization": "Bearer " + token
#     }

#     res = requests.get(url=searchUrl, headers=headers)

#     resd = json.dumps(res.json(), indent=2)

#     #print(resd)
#     A = []
#     for i in range(min(length, len(res.json()["tracks"]["items"]))):
#         parsed = res.json()
#         A.append({
#             "title": parsed["name"],
#             "artist": parsed["artists"][0]["name"],
#             "cover_url": getImage(["album"]["id"], token),
#             "slug": parsed["tracks"]["items"][i]["id"],
#         })
#     return A




def musics (response, music_slug): 
    song = {}
    try:
        song = Song.objects.filter(spotId=music_slug)[0]
    except:
        print("Song not found, creating ...")
        token = setUp()

        objs = getID(music_slug, token)
        print(objs)

        try:
            artist = Author.objects.filter(spotId=objs["artist"]["main"]["id"])[0]
        except:
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
                feats.append(Author.objects.filter(spotId=feat["id"])[0])
            except:
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
            album = Album.objects.filter(spotId=objs["album"]["id"])[0]
        except:
            print("Album not found, creating ...")
            Album.objects.create(
                spotId=objs["album"]["id"], 
                name=objs["album"]["name"],
                image=objs["album"]["image"],
                link=objs["album"]["spotify"],
                dat=objs["album"]["release_date"],
            )
            album = Album.objects.filter(spotId=objs["album"]["id"])[0]

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
        # print(artist)
        # song.author.set([artist])
        # song.album.set([album])
        # song.save()
        # song.feats.set(feats)

    # try:
    profile = {"prof": Profile.objects.filter(user=response.user)[0], "is_connected": True}
    # except:
    #     profile = {"is_connected": False}

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

    try:
        profile2 = {"prof": Profile.objects.filter(user=response.user)[0], "is_connected": True}
        favs = Fav.objects.filter(user=profile2["prof"])
        isLiked = False
        for fav in favs:
            if fav.song == song:
                isLiked = True
    except:
        isLiked = False

    return render(response, "musics/index.html", {"song": song, "author": song.author, "album": song.album, "profile": profile, "is_liked": isLiked})