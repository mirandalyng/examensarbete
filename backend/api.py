from fastapi import FastAPI, HTTPException, Query
from utils.filter_decades import filter_by_decades, get_decades
from utils.filter_genres import get_genres, filter_by_genre
from utils.num_tracks import num_of_tracks
from load_lancedb import load_lancedb


# load lancedb database
df = load_lancedb()


# count options for number of tracks
COUNT_OPTIONS = [10, 15, 20, 25, 30]


app = FastAPI()

# Endpoint for filters (decades, genres, option for number of songs)


@app.get("/filter")
async def get_filters():
    return {
        "decades": get_decades(df),
        "genres": get_genres(df),
        "count": COUNT_OPTIONS,
    }

# Enpoint for tracks


@app.get("/tracks")
async def get_tracks(
    count: int = Query(20, ge=10, le=30),  # default 10
    decades: list[int] | None = Query(None),
    genres: list[str] | None = Query(None),
    seed: int | None = None,  # Seed to be able to generate exactly the same quiz again
):
    result = num_of_tracks(df, count, decades, genres, seed)
    if result.empty:
        raise HTTPException(status_code=404, detail="No matching tracks found")

    result["genres"] = result["genres"].apply(list)
    return result.to_dict(orient="records")
