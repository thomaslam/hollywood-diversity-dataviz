import pandas as pd
import os

merged_df = pd.DataFrame()
movies_dir = "./data/movies"
for filename in os.listdir(movies_dir):
    movie_df = pd.read_csv(movies_dir + "/" + filename)
    print(filename)
    merged_df = pd.concat([merged_df, movie_df], ignore_index=True)

merged_df.to_csv("./data/movie_merged_full.csv")