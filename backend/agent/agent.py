from agent.deps import FollowUps, MusicData
from agent.model import nvidia_model
from pydantic_ai import Agent

model = nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b")

music_agent = Agent(
    model=model,
    deps_type=MusicData,
    output_type=FollowUps,
    system_prompt=(
        "You are a quiz master. You will be provided with metadata for a song (MusicTrack).\n"
        "Create ONE tricky follow-up question based on this metadata, generate 4 plausible multiple-choice options, "
        "and indicate which one is correct.\n"
        "IMPORTANT: NEVER reveal the artist's name or the song title in the question text itself, "
        "as the player is expected to guess it as the final answer in the next step of the UI!"
    ),
)
