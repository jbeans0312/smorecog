import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["figure.figsize"] = [7.50, 3.40]
plt.rcParams["figure.autolayout"] = True

headers = ['danceability', 'energy', 'key', 'loudness',
           'mode', 'speechiness', 'acousticness',
           'instrumentalness', 'liveness', 'valence',
           'tempo', 'type', 'id', 'uri', 'track_href',
           'analysis_url', 'duration_ms', 'time_signature']

df = pd.read_csv('./smog_data/smog.csv', names=headers)
