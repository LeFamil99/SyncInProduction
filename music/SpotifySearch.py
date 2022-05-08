import requests
import base64
import json
from music.secrets import *

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


def getID(query): 
    token = setUp()
    
    length = 10

    searchUrl = f"https://api.spotify.com/v1/search?q=track:{query}&type=track&limit={length}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)

    #print(resd)
    A = []
    for i in range(min(length, len(res.json()["tracks"]["items"]))):
        A.append(res.json()["tracks"]["items"][i]["id"])
    return A

def getName(id):
    token = setUp()
    
    length = 10

    searchUrl = f"https://api.spotify.com/v1/tracks/{id}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)
    
    print(resd)
    return res.json()["name"]

def getAlbum(id):
    token = setUp()
    
    length = 1

    searchUrl = f"https://api.spotify.com/v1/tracks/{id}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)

    #print(resd)
    return res.json()["album"]["external_urls"]["spotify"]

def getAlbumID(id):
    token = setUp()

    searchUrl = f"https://api.spotify.com/v1/tracks/{id}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)

    #print(resd)
    return res.json()["album"]["id"]

def getImage(albumID):
    token = setUp()
    
    searchUrl = f"https://api.spotify.com/v1/albums/{albumID}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)

    print(resd)
    return res.json()["images"][0]["url"]
    
def getMainArtist(id):
    token = setUp()
    
    searchUrl = f"https://api.spotify.com/v1/tracks/{id}"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=searchUrl, headers=headers)

    resd = json.dumps(res.json(), indent=2)

    print(resd)
    return res.json()["artists"][0]["name"]

print(getImage(getAlbumID(getID("runaway")[0])))
#print(getImage(getAlbumID(getID("hotel california")[0])))
print(setUp())
print(getAlbumID(getID("runaway")[0]))