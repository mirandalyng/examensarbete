from backend.agent.agent import music_agent
from backend.agent.deps import MusicData
import asyncio
import logfire
from agent.prompts import get_prompt


# Connect to Logfire
# logfire.configure()
# logfire.instrument_system_metrics()
logfire.instrument_pydantic_ai()


async def main(prompt: str, deps: MusicData):
    result = await music_agent.run(prompt, deps=deps)
    print(result.output)


# Test
if __name__ == "__main__":
    test_track = MusicData(
    spotify_url="...",
    track_name="Dancing Queen",
    title_normalized="Dancing Queen",
    primary_artist="ABBA",
    artist_list=["ABBA"],
    genres=["pop"],
    release_year=1976,
    decade=1970,
    album="Arrival",
    artist_popularity=85,
    track_popularity=80,
)
    asyncio.run(
        main("Skapa en följdfråga om vilka som är med i bandet.", test_track))
