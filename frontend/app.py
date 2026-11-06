import streamlit as st
from utils.lancedb_conn import load_lancedb
from utils.filter_decades import filter_by_decades, get_decades

# loads lancedb file


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
