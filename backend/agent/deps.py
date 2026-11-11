from pydantic import BaseModel

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

# The structure for the followup questions
class FollowUps(BaseModel):
    question: str
    option: list[str]
    correct_answer: str
