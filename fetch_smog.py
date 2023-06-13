import spotipy
import os
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

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


def get_playlist_tracks_more_than_100_songs(uri):
    results = sp.playlist_items(uri)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    results = tracks

    playlist_tracks_id = []
    playlist_tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []
    playlist_tracks_first_release_date = []
    playlist_tracks_popularity = []
    with tqdm(total=len(results)) as pbar:
        for i in range(len(results)):

            if i == 0:
                playlist_tracks_id = results[i]['track']['id']
                playlist_tracks_titles = results[i]['track']['name']
                playlist_tracks_first_release_date = results[i]['track']['album']['release_date']
                playlist_tracks_popularity = results[i]['track']['popularity']

                artist_list = []
                for artist in results[i]['track']['artists']:
                    artist_list = artist['name']
                playlist_tracks_artists = artist_list

                features = sp.audio_features(playlist_tracks_id)
                features_df = pd.DataFrame(data=features, columns=features[0].keys())
                features_df['title'] = playlist_tracks_titles
                features_df['all_artists'] = playlist_tracks_artists
                features_df['popularity'] = playlist_tracks_popularity
                features_df['release_date'] = playlist_tracks_first_release_date
                features_df = features_df[['id', 'title', 'all_artists', 'popularity', 'release_date',
                                           'danceability', 'energy', 'key', 'loudness',
                                           'mode', 'acousticness', 'instrumentalness',
                                           'liveness', 'valence', 'tempo',
                                           'duration_ms', 'time_signature']]
                continue
            else:
                try:
                    playlist_tracks_id = results[i]['track']['id']
                    pbar.set_description(f'Processing: {playlist_tracks_id}')
                    pbar.update(1)
                    playlist_tracks_titles = results[i]['track']['name']
                    playlist_tracks_first_release_date = results[i]['track']['album']['release_date']
                    playlist_tracks_popularity = results[i]['track']['popularity']
                    artist_list = []
                    for artist in results[i]['track']['artists']:
                        artist_list = artist['name']
                    playlist_tracks_artists = artist_list
                    features = sp.audio_features(playlist_tracks_id)
                    new_row = {'id': [playlist_tracks_id],
                               'title': [playlist_tracks_titles],
                               'all_artists': [playlist_tracks_artists],
                               'popularity': [playlist_tracks_popularity],
                               'release_date': [playlist_tracks_first_release_date],
                               'danceability': [features[0]['danceability']],
                               'energy': [features[0]['energy']],
                               'key': [features[0]['key']],
                               'loudness': [features[0]['loudness']],
                               'mode': [features[0]['mode']],
                               'acousticness': [features[0]['acousticness']],
                               'instrumentalness': [features[0]['instrumentalness']],
                               'liveness': [features[0]['liveness']],
                               'valence': [features[0]['valence']],
                               'tempo': [features[0]['tempo']],
                               'duration_ms': [features[0]['duration_ms']],
                               'time_signature': [features[0]['time_signature']]
                               }

                    dfs = [features_df, pd.DataFrame(new_row)]
                    features_df = pd.concat(dfs, ignore_index=True)
                except:
                    continue

    return features_df


print('Scraping smog data')
smog_df = get_playlist_tracks_more_than_100_songs(smog_URI)
smog_df = smog_df.dropna()
smog_df.to_csv('./smog_data/smog.csv', index=False, encoding='utf8')


