from django.shortcuts import render
import requests
import base64
import json
from secrets import *

# Create your views here.

def search (response): 
    return render(response, "search/index.html", {})

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


def getID(query, token, lengthh, offset): 
    
    length = lengthh + 1

    l2 = min(length + offset, 50)

    searchUrl = f"https://api.spotify.com/v1/search?q=track:{query}&type=track&limit={l2}&offset={offset}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)

    print(length, offset, resd)
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
    
    searchUrl = f"https://api.spotify.com/v1/albums/{albumID}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)

    return res.json()["images"][0]["url"]

# def getName(id, token):
    
#     length = 10

#     searchUrl = f"https://api.spotify.com/v1/tracks/{id}"
#     headers = {
#         "Authorization": "Bearer " + token
#     }

#     res = requests.get(url=searchUrl, headers=headers)

#     resd = json.dumps(res.json(), indent=2)
    
#     return res.json()["name"]



def results (response, offset = 0): 
    offset = int(offset)
    #print(query)
    query = None

    #if response.method == "GET":
    query = response.GET.get("vlad")
    


    token = setUp()

    objs = getID(query, token, 5 if offset == 0 else 10, offset)

    return render(response, "results/index.html", {"query": query, "results": objs})