import lancedb
from pathlib import Path
import pandas as pd


ROOT_PATH = Path(__file__).resolve().parents[2] / "backend" / "data"


def load_lancedb() -> pd.DataFrame:
    # connect to lancedb

    db = lancedb.connect(ROOT_PATH / "music_quiz")
    # read in lancedb file
    table = db.open_table("quiz")
    # convert it to dataframe in pandas to be able to call it in our filter functions
    return table.to_pandas()
