import pandas as pd

smog_df = pd.read_csv('./smog_data/smog.csv')
smog_df.head()
smog_df['y'] = 1

y_train = smog_df.iloc[:, :-1]

user_df = pd.read_csv('./smog_data/user.csv')
user_df.head()

feature_cols = ['danceability', 'energy', 'key', 'loudness',
                'mode', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'tempo', 'duration_ms',
                'time_signature']


# normalizing the dataset
scaler = StandardScaler()




