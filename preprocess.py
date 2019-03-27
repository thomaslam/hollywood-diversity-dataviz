import pandas as pd

df = pd.read_csv('./datasets/movie_metadata.csv')
print(df.shape)
df = df.drop(['color', 'facenumber_in_poster', 'aspect_ratio'], axis=1)
print(df.shape)
        