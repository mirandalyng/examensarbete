from model import nvidia_model
from pydantic_ai import Agent
import pandas as pd
from pydantic import BaseModel

model = nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b")

music_agent = Agent(
    model = model, 
    instructions=("You are a music quiz expert that provides questions based of a subset of tracks with information"))




#df = pd.read_parquet("../../data/serving/mart.parquet", encoding="utf-8")






    