from .deps import FollowUps, MusicData
from .model import nvidia_model
from .prompts import get_prompt
from pydantic_ai import Agent, RunContext

model = nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b")

music_agent = Agent(
    model=model,
    deps_type=MusicData,
    output_type=FollowUps,
    instructions=(get_prompt()
    ),
)

# Dynamic instructions: runs on every agent.run() and adds the track data
# from MusicData (deps) to the instructions, so the agent can base its
# follow-up questions and correct answers on real data instead of guessing.
# The static prompt from Logfire is combined with this text.
@music_agent.instructions
def track_context(ctx: RunContext[MusicData]) -> str:
    d = ctx.deps
    return (
        f"Låt: {d.track_name}\nArtist: {d.artist_names}\n"
        f"Album: {d.album}\nÅr: {d.release_year}\nGenrer: {', '.join(d.genres)}"
    )


        # system_prompt=(
        # "You are a quiz master. You will be provided with metadata for a song (MusicTrack).\n"
        # "Create ONE tricky follow-up question based on this metadata, generate 4 plausible multiple-choice options, "
        # "and indicate which one is correct.\n"
        # "IMPORTANT: NEVER reveal the artist's name or the song title in the question text itself, "
        # "as the player is expected to guess it as the final answer in the next step of the UI!"),