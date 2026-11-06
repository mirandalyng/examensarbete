from frontend.utils.filter_decades import filter_by_decades
from frontend.utils.filter_genres import filter_by_genre
from frontend.utils.randomize import randomize
import pandas as pd


def num_of_tracks(df, count, decades=None, genres=None, seed=None) -> pd.DataFrame:

    pool = df
    if decades:
        pool = filter_by_decades(pool, decades)
    if genres:
        pool = filter_by_genre(pool, genres)

    return randomize(pool, count, seed)
