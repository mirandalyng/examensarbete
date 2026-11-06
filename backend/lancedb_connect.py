""" Create vectors and connect to LanceDB """

import pandas as pd
from pathlib import Path
import lancedb  # The main database connection and operations
# LanceModel: Pydantic model for defining table schemas. Vector: Field type for storing vector embeddings
from lancedb.pydantic import LanceModel, Vector
# get_registry(): Access to the embedding function registry. It has all the supported as well as custom embedding functions registered by the user
from lancedb.embeddings import get_registry

# Create path and read parquet file
ROOT = Path(__file__).resolve().parent.parent   # examensarbete/
DATA_PATH = ROOT / "data" / "serving"
df = pd.read_parquet(DATA_PATH / "mart.parquet")

""" ---- Connect to LanceDB ---- 
database locally: uri is the name of the searchroot on the 
folder where lancedb will save the files.
"""

DB_PATH = Path(__file__).parent / "data" / "music_quiz"
db = lancedb.connect(uri=str(DB_PATH))


""" ---- Initialize the Embedding Function ----
- Coose and configure ypur embedding model
This creates an embedding function from the local embedding registry. 
The Python snippet uses the sentence-transformers provider with the BGE model; 
the TypeScript snippet uses the Transformers-backed huggingface provider
"""


model = get_registry().get("sentence-transformers").create(
    name="sentence-transformers/static-similarity-mrl-multilingual-v1"
)

""" ---- Define your schema ---- 
Create a Pydantic model that defines your table structure:
- SourceField(): This field will be embedded
- VectorField(): This stores the embeddings
- model.ndims(): Sets vector dimensions for your model
"""


# create a textcolumn from columns in dataset for better search
df["search_text"] = (
    "song_name: " + df["track_name"] +
    ", artist_name: " + df["artist_names"] +
    ", genre: " + df["genres"].apply(", ".join) +
    ", album: " + df["album"]
)


class Quiz(LanceModel):
    spotify_url: str
    track_id: str
    artist_id: str
    track_name: str
    release_year: int
    decade: int
    track_popularity: int
    artist_names: str
    artist_popularity: int
    genres: list[str]
    album: str

    # search vector is created from the text that is put togetgher search text
    search_text: str = model.SourceField()
    # model.ndims() asks the model how many number/dimensions that will be in the vector
    vector: Vector(model.ndims()) = model.VectorField()


""" ---- Create table and ingest data ---- """
# use mode = "overwrite" if anything changes in the dataset
quiz_table = db.create_table("quiz", schema=Quiz, data=df, mode="overwrite")
