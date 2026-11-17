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
        spotify_url="https://open.spotify.com/track/xxxx",
        artist_id="xxxx",
        artist_names="ABBA",
        track_name="Dancing Queen",
        genres=["swedish pop", "disco"],
        release_year=1976,
        decade=1970,
        album="Arrival",
        artist_popularity=80,
        track_popularity=85,
    )
    asyncio.run(
        main("Skapa en följdfråga om vilka som är med i bandet.", test_track))
