import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MinMaxScaler

smog_df = pd.read_csv('./smog_data/smog.csv')
smog_df.head()

user_df = pd.read_csv('./smog_data/user.csv')
user_df.head()

feature_cols = ['danceability', 'energy', 'key', 'loudness',
                'mode', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'tempo', 'duration_ms',
                'time_signature']


# normalizing the dataset
scaler = MinMaxScaler()
normalized_df = scaler.fit_transform(smog_df[feature_cols])

# generate cosine similarity matrix
indices = pd.Series(smog_df.index, index=smog_df['title']).drop_duplicates()

