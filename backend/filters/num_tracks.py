from filter_decades import filter_by_decades
from filter_genres import filter_by_genre
from randomize import randomize
from load_df import load_tracks
import pandas as pd

df = load_tracks()


def num_of_tracks(df, count, decades=None, genres=None, seed=None) -> pd.DataFrame:

    pool = df
    if decades:
        pool = filter_by_decades(pool, decades)
    if genres:
        pool = filter_by_genre(pool, genres)

    return randomize(pool, count, seed)
