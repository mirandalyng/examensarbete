import pandas as pd


def get_genres(df: pd.DataFrame) -> list[str]:
    """Alla genres som finns i datan, sorterade (till selectbox/multiselect)."""
    return sorted(df["genres"].explode().dropna().unique().tolist())

# No genre selected (None) -> no filtering, return all tracks


def filter_by_genre(df: pd.DataFrame, genres: str | list[str]) -> pd.DataFrame:
    if genres is None:
        return df

    # If the user passed a single genre as a string (e.g. "jazz"),
    # wrap it in a list so the rest of the function can treat everything as a list
    if isinstance(genres, str):
        genres = [genres]

    # Empty list -> no genre selected, so again return all tracks
    if len(genres) == 0:
        return df

    # Build a set of the wanted genres, normalized:
    # A set is used because "x in set" is much faster than "x in list"
    wanted = {g for g in genres}

    # Build a boolean mask (one True/False per row in the DataFrame).
    # Each cell in df["genres"] is itself a list (or numpy array) of genres,
    # e.g. ["hip hop", "funk"], so we check every row separately with apply().
    mask = df["genres"].apply(
        # For a row's genre list, return True if ANY of its genres
        # (normalized the same way) is in the wanted set.
        # This makes the filter an OR: a track matches if it has at least
        # one of the selected genres.
        lambda row: any(g in wanted for g in row)
        # Guard: only do the check if the cell is not None and not empty
        if row is not None and len(row) > 0
        # Tracks with no genres (None or []) can never match, so mark them False
        else False
    )

    # Keep only the rows where the mask is True
    return df[mask]
