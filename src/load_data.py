import pandas as pd 
import numpy as np

df = pd.read_csv('C:/Users/bogda/OOPCurseWork/movie_project/data/movies.csv')
df2 = df.replace(r'^\s*$', np.nan, regex=True)
df_clean = df2.dropna()
df_clean.drop(columns=["released", "votes",'rating'], inplace=True)

films_dict = df_clean.to_dict(orient="records")