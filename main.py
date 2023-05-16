import spotipy
from dotenv import load_dotenv
import os
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
    tracks = [x["track"]["uri"] for x in tracks_response["items"]]
    while tracks_response["next"]:
        tracks_response = sp.next(tracks_response)
        tracks.extend([x["track"]["uri"] for x in tracks_response["items"]])
    return tracks


t = get_all_tracks(smog_URI)
playlist_size = len(t)
print(t)
print(playlist_size)