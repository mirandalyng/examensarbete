from backend.agent.agent import music_agent
from backend.agent.deps import MusicData
import asyncio
import logfire

# Connect to Logfire
# logfire.configure()
# logfire.instrument_system_metrics()
logfire.instrument_pydantic_ai()

PROMPT = "Skapa en följdfråga om vilka som är med i bandet/vem artisten är"

def track(title, artist, year, genres, album, artist_pop, track_pop, artists=None):
    return MusicData(
        spotify_url="...", 
        track_name=title,
        title_normalized=title,
        primary_artist=artist,
        artist_list=artists or [artist],
        genres=genres,
        release_year=year,
        decade=year // 10 * 10,
        album=album,
        artist_popularity=artist_pop,
        track_popularity=track_pop,
    )

TEST_TRACKS = {
    "mellan_70tal": track("Dancing Queen", "ABBA", 1976, ["pop"], "Arrival", 85, 80),
    "känd_80tal": track("Billie Jean", "Michael Jackson", 1982, ["pop"], "Thriller", 95, 92),
    "känd_90tal": track("Smells Like Teen Spirit", "Nirvana", 1991, ["grunge"], "Nevermind", 92, 91),
    "flera_artister": track("Under Pressure", "Queen", 1981, ["rock"], "Hot Space", 85, 82,
                            artists=["Queen", "David Bowie"]),
    "latin_2017": track("Despacito", "Luis Fonsi", 2017, ["latin"], "Vida", 85, 88,
                        artists=["Luis Fonsi", "Daddy Yankee"]),
    "svenska": track("Känn ingen sorg för mig Göteborg", "Håkan Hellström", 2002,
                     ["swedish"], "Känn ingen sorg för mig Göteborg", 70, 55),
    "saknar_album": track("Take Five", "The Dave Brubeck Quartet", 1959, ["jazz"], "Missing album", 70, 65),
    "okänd": track("Obscure Demo Track", "Unknown Band", 1987, ["synth-pop"], "Missing album", 12, 5),
}

async def main():
    for name, deps in TEST_TRACKS.items():
        with logfire.span("playground test: {name}", name=name):
            try:
                result = await music_agent.run(PROMPT, deps=deps)
                print(f"\n=== {name} ===\n{result.output.model_dump_json(indent=2)}")
            except Exception as e:
                print(f"\n=== {name} FEL: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(main())




# async def main(prompt: str, deps: MusicData):
#     result = await music_agent.run(prompt, deps=deps)
#     print(result.output)


# # Test
# if __name__ == "__main__":
#     test_track = MusicData(
#     spotify_url="...",
#     track_name="Dancing Queen",
#     title_normalized="Dancing Queen",
#     primary_artist="ABBA",
#     artist_list=["ABBA"],
#     genres=["pop"],
#     release_year=1976,
#     decade=1970,
#     album="Arrival",
#     artist_popularity=85,
#     track_popularity=80,
# )
#     asyncio.run(
#         main("Skapa en följdfråga om vilka som är med i bandet.", test_track))
