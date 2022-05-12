from django.shortcuts import render
import requests
import base64
import json
from secrets import *

# Create your views here.

def search (response): 
    # Retourne la vue
    return render(response, "search/index.html", {})

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


def getAllInfos(query, token, lengthh, offset): 
    """Génère toutes les infos nécessaires sur plusieurs chansons trouvées à l'aide d'un query

    Args:
        query (String): query de la recherche de chansons
        token (_type_): Token d'accès à l'API de Spotify
        lengthh (Integer): Nombre de chansons
        offset (Integer): In dex de départ pour trouver les chansons

    Returns:
        dict: Dictionnaire contenant toutes les infos
    """

    length = lengthh + 1
    l2 = min(length + offset, 50)

    # Requête des infos sur la chanson par le biais de l'API Spotify
    searchUrl = f"https://api.spotify.com/v1/search?q=track:{query}&type=track&limit={l2}&offset={offset}"
    headers = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(url=searchUrl, headers=headers)
    resd = json.dumps(res.json(), indent=2)
    print(length, offset, resd)

    # Crée un array contenant toutes les infos sur toutes les chansons 
    A = []
    for i in range(min(length, len(res.json()["tracks"]["items"]))):
        parsed = res.json()
        A.append({
            "title": parsed["tracks"]["items"][i]["name"],
            "artist": parsed["tracks"]["items"][i]["artists"][0]["name"],
            "cover_url": getImage(parsed["tracks"]["items"][i]["album"]["id"], token),
            "slug": parsed["tracks"]["items"][i]["id"],
        })
    if len(A) == lengthh + 1:
        A.pop()
        return {"A": A, "plus": True, "next_offset": offset + lengthh}
    else:
        return {"A": A, "plus": False}


def getImage(albumID, token):
    """Génère l'URL de l'image d'un album

    Args:
        albumID (String): ID Spotify de l'album
        token (String): Token d'accès à l'API de Spotify

    Returns:
        String: URL de l'image
    """
    
    searchUrl = f"https://api.spotify.com/v1/albums/{albumID}"
    headers = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(url=searchUrl, headers=headers)
    resd = json.dumps(res.json(), indent=2)

    # Génère et retourne l'URL de l'image
    return res.json()["images"][0]["url"]


def results (response, offset = 0): 

    offset = int(offset)
    query = None

    # Obtenir le query de la barre de recherche de la page qui appelle celle-ci
    query = response.GET.get("vlad")
    
    # Génération du token
    token = setUp()


    objs = getAllInfos(query, token, 5 if offset == 0 else 10, offset)

    # Retourne la vue
    return render(response, "results/index.html", {"query": query, "results": objs})