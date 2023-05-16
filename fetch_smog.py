import spotipy
import os
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

# spotipy authentication
client_credentials_manager = \
    SpotifyClientCredentials(client_id=os.getenv("SECRET1"), client_secret=os.getenv("SECRET2"))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# now that we are authenticated we can access da api
# scrape the smog tracks
smog_link = "https://open.spotify.com/playlist/1LF6XeBlaD0yrDQ0t5rdEb?si=7a138d8c8c3540fb"
smog_URI = smog_link.split('/')[-1].split('?')[0]


# get all tracks on playlist (boo spotify api query limits)
def get_all_tracks(uri):
    tracks_response = sp.playlist_items(uri)
    t = sp.audio_features(x["track"]["uri"] for x in tracks_response["items"])
    while tracks_response["next"]:
        tracks_response = sp.next(tracks_response)
        t.extend(sp.audio_features(x["track"]["uri"] for x in tracks_response["items"]))
    return t


tracks = get_all_tracks(smog_URI)
playlist_size = len(tracks)

p = Path(r'./smog_data/tracks_out.json')
with p.open('r', encoding='utf-8') as f:
    data = json.loads(f.read())

df = pd.json_normalize(data)
df = df.dropna()
df.to_csv('./smog_data/smog.csv', index=False, encoding='utf8')
