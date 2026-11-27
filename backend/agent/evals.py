from agent import music_agent, MusicData
from pydantic_evals.evaluators import LLMJudge, Evaluator, MaxDuration, MaxModelRequests, EvaluatorContext
from pydantic_evals import Dataset, Case    
from dataclasses import dataclass
from model import nvidia_model
from deps import FollowUps
import asyncio

model = nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b")

@dataclass
class RAGInput:
    prompt: str
    client: FollowUps

dataset = Dataset(
    name='language_evaluation',
    cases=[
        Case(
            inputs=RAGInput(
                prompt='?',
                client='France is a country in Europe. Its capital is Paris.',
            ),
        ),
    ],
    evaluators=[
        LLMJudge(
            rubric='Response answers the prompt= using only information from the provided client=',
            include_input=True,
            assertion={'evaluation_name': 'grounded', 'include_reason': True},
        ),
        LLMJudge(
            rubric='Response cites specific quotes or facts from the client=',
            include_input=True,
            assertion={'evaluation_name': 'uses_citations', 'include_reason': True},
        ),
    ],
)