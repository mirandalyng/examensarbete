import pandas as pd


def randomize(df: pd.DataFrame, count: int, seed: int | None = None) -> pd.DataFrame:
    """Pick up to `count` random tracks from an already filtered dataframe."""
    # Never ask for more rows than exist, otherwise sample() raises an error
    n = min(count, len(df))

    # Pick n random rows. Same seed + same data = same result (None = different every time)
    sampled = df.sample(n=n, random_state=seed)

    # Reset the index to 0, 1, 2... because sample() keeps the old row numbers
    return sampled.reset_index(drop=True)
