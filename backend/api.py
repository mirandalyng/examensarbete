import pandas as pd
from agent.agent import music_agent
from agent.deps import MusicData
from fastapi import FastAPI, HTTPException, Query
from utils.filter_decades import get_decades
from utils.filter_genres import get_genres
from utils.num_tracks import num_of_tracks

# load lancedb database
df = pd.read_parquet("../data/serving/mart.parquet")


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


# Endpoint for tracks


@app.get("/tracks", response_model=list[MusicData])
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


@app.post("/generated_quiz")
async def generate_quiz(tracks: list[MusicData]):
    if not tracks:
        return []
    tracks.sort(key=lambda x: (x.track_popularity + x.artist_popularity), reverse=True)

    half_of_tracks = max(1, len(tracks) // 2)
    popular_tracks = tracks[:half_of_tracks]

    generated_quiz = []
    for track in popular_tracks:
        result = await music_agent.run(
            f"Generate a follow-up question from this track: {track.model_dump()}",
            deps=track,
        )

        generated_quiz.append(
            {
                "answer_artist": track.artist_names,
                "answer_track": track.track_name,
                "answer_followup_quistion": result.output.model_dump(),
            }
        )

    return generated_quiz
