from fastapi import APIRouter, HTTPException
import requests
from spotify_auth import get_access_token
import os

router = APIRouter()

PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID")

@router.get("/playlist")
def get_playlist():
    token = get_access_token()
    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail="Playlist not found")
    data = res.json()
    return {
        "name": data["name"],
        "image": data["images"][0]["url"] if data["images"] else None,
        "tracks": [
            {
                "name": t["track"]["name"],
                "artist": t["track"]["artists"][0]["name"],
                "id": t["track"]["id"]
            } for t in data["tracks"]["items"] if t["track"]
        ]
    }

@router.get("/now-playing")
def now_playing():
    token = get_access_token()
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    if res.status_code == 204:
        return {"status": "no music playing"}
    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail="Fehler beim Abrufen")
    item = res.json()["item"]
    return {
        "name": item["name"],
        "artist": item["artists"][0]["name"],
        "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None
    }

@router.get("/up-next")
def up_next():
    token = get_access_token()
    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail="Fehler beim Abrufen")
    data = res.json()
    tracks = [
        {
            "name": t["track"]["name"],
            "artist": t["track"]["artists"][0]["name"]
        } for t in data["items"] if t["track"]
    ]
    return {"tracks": tracks[:5]}
