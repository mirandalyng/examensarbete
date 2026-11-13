from pydantic import BaseModel, Field


# The structured data that the agent recives
class MusicData(BaseModel):
    spotify_url: str
    artist_id: str
    artist_names: str
    track_name: str
    genres: list[str]
    release_year: int
    decade: int
    album: str
    artist_popularity: int
    track_popularity: int


# The structure for the followup questions
class FollowUps(BaseModel):
    question: str = Field(description="Question about the song or artist."
                          "Information is to be fetched from the internet. Do not include the right answer in the question.")
    option: list[str] = Field(description="options can be 2-4.")
    correct_answer: str = Field(
        description="The correct answer of the questin. Must be included in the options.")
