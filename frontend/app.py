
#############
# imports and comments underneith must be in this order for the search paths to work!
###########
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st  # noqa: E402
from backend.load_lancedb import load_lancedb  # noqa: E402  # isort: skip
from utils.filter_decades import filter_by_decades, get_decades  # noqa: E402  # isort: skip


@st.cache_data
def get_data():
    return load_lancedb()


df = get_data()

list_decades = get_decades(df)

selected_decades = st.multiselect(
    "Select decade",
    options=[dec for dec in list_decades],
    default=[]
)

st.write("valda:", selected_decades, "dtype:", df["decade"].dtype)
filtered_df = filter_by_decades(df, selected_decades)
st.write("rader efter filter:", len(filtered_df), "av", len(df))

# Dataframe
st.dataframe(filtered_df)
