import lancedb
from pathlib import Path
import pandas as pd


DB_PATH = Path(__file__).resolve().parent / "data" / "music_quiz"


def load_lancedb() -> pd.DataFrame:
    # connect to lancedb

    db = lancedb.connect(DB_PATH)
    # read in lancedb file
    table = db.open_table("quiz")

    # Drop the vector column before it reaches Streamlit.
    # Filters only need decade/genres, and the vectors (~780 MB) made
    # st.cache_data's copy on every rerun slow.
    # Vector search still works: table.search() reads the vectors from LanceDB.
    return table.to_pandas().drop(columns=["vector"])
