from .deps import FollowUps, MusicData
from .model import nvidia_model
from .prompts import get_prompt
from pydantic_ai import Agent, RunContext
from .tools import search_wikipedia
import logfire


logfire.instrument_pydantic_ai()
logfire.instrument_httpx()


model = nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b")

music_agent = Agent(
    model=model,
    deps_type=MusicData,
    output_type=FollowUps,
    instructions=(get_prompt()),
    tools=[search_wikipedia],
)


""" 
Dynamic instructions: runs on every agent.run() and adds the track data
from MusicData (deps) to the instructions, so the agent can base its
follow-up questions and correct answers on real data instead of guessing.
The static prompt from Logfire is combined with this text.
"""

@music_agent.instructions
def track_context(ctx: RunContext[MusicData]) -> str:
    d = ctx.deps
    return (
        f"Låt: {d.track_name}\nArtist: {d.artist_names}\n"
        f"Album: {d.album}\nÅr: {d.release_year}\nGenrer: {', '.join(d.genres)}"
    )
