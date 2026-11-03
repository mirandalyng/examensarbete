import pandas as pd
from pathlib import Path
from load_df import load_tracks

df = load_tracks()

# DECADES
def get_decades(df: pd.DataFrame) -> list[int]:
    """Alla årtionden som finns i datan, sorterade (till selectbox/multiselect)."""
    return sorted(df["decade"].dropna().astype(int).unique().tolist())


def filter_by_decades(df: pd.DataFrame, decades: int | list[int]) -> pd.DataFrame:
    """
    Returnerar låtar från ett eller flera årtionden.

    decades kan vara ett enskilt årtionde (1980) eller en lista ([1980, 1990]).
    Tom lista eller None ger hela DataFrame:n (inget filter).
    """
    if decades is None:
        return df

    if isinstance(decades, int):
        decades = [decades]

    if len(decades) == 0:
        return df

    return df[df["decade"].isin(decades)]
