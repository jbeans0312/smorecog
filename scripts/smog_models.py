import pandas as pd

smog_df = pd.read_csv('smog_data/pretty_smog.csv')
smog_df.head()

feature_cols = ['danceability', 'energy', 'key', 'loudness',
                'mode', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'tempo',
                'time_signature']




