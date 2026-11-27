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
    is_famous = d.artist_popularity > 90 and d.track_popularity > 90
    mode = (
        "Give no options (options = null). correct_answer should be short with only one answer "
        if is_famous
        else "Give EXACTLY 3 options"
    )
    lines = [
        f"Låt: {d.title_normalized}",
        f"Huvudartist: {d.primary_artist}",
        f"Alla artister: {', '.join(d.artist_list)}",
        f"År: {d.release_year}",
        f"Genrer: {', '.join(d.genres)}",
    ]
    if d.album != "Missing album":
        lines.insert(3, f"Album: {d.album}")
    lines.append(f"Frågeformat: {mode}")
    return "\n".join(lines)