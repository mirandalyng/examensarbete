
import streamlit as st
import requests

# base URL for API
API_URL = "http://127.0.0.1:8000"

# Load filters from get endpoint filter


@st.cache_data(ttl=300)
def load_filters():
    filter = requests.get(f"{API_URL}/filter", timeout=30)
    filter.raise_for_status()
    return filter.json()


# Filters from load filters displayed in selections , returns the count, decade , genre
def filters():
    filters = load_filters()

    decades = st.multiselect("Decade", options=filters["decades"])
    genres = st.multiselect("Genre", options=filters["genres"])
    count = st.selectbox(
        "Number of tracks", options=filters["count"])

    return count, decades, genres

# Fetches random selection of songs from the API - empty list if nothing matches


def fetch_tracks(count: int, decades: list[int], genres: list[str]) -> list[dict]:
    params = {
        "count": count,
        "decades": decades,
        "genres": genres
    }

    tracks = requests.get(f"{API_URL}/tracks", params=params, timeout=30)
    if tracks.status_code == 404:
        return []

    tracks.raise_for_status()

    return tracks.json()

# Main function to display the quiz


def display_quiz():
    st.markdown("# Welcome!")

    count, decades, genres = filters()

    if st.button("Generate Quiz"):
        tracks = fetch_tracks(count, decades, genres)

        if not tracks:
            st.warning("No tracks matches filter, try something else")
        else:
            st.session_state["tracks"] = tracks

    if "tracks" in st.session_state:
        tracks = st.session_state["tracks"]

        st.dataframe(tracks)


if __name__ == '__main__':

    display_quiz()
