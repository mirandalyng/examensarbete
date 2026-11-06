import pandas as pd
from pathlib import Path

PARQUET = Path("../data/serving/mart.parquet")


def load_tracks() -> pd.DataFrame:
    """Read the whole parquete file."""
    return pd.read_parquet(PARQUET)
