from pydantic import BaseModel, model_validator


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


# The structure for the follow-up questions.
# Some questions are multiple choice (with options), others are open
# questions where the user types the answer (options is None).
class FollowUps(BaseModel):
    question: str
    # Optional: None (or left out) means an open question without alternatives
    options: list[str] | None = None
    correct_answer: str

    # Validator: runs automatically after the model has returned its answer
    # (mode="after" means all fields are already filled in and type-checked)
    @model_validator(mode="after")
    def answer_in_options(self):
        # Only check the options if the question actuallt has any
        # Open questions (options is None) skip the check
        if self.options is not None and self.correct_answer not in self.options:
            raise ValueError("correct_answer must be one of options")
        return self
