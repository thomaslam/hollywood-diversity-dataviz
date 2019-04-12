import pandas as pd

merged_df = pd.read_csv("./data/movie_merged.csv")
merged_df = merged_df[merged_df['title_year'] > 1995]
merged_df.to_csv("./data/movie_merged.csv")