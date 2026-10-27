import dlt
import pandas as pd
from pathlib import Path

"""Pipeline to load raw csv-files into Duckdb """

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw"

def csv_resource(table: str, filename: str):
    @dlt.resource(name=table, write_disposition="replace")
    def read_data():
        for chunk in pd.read_csv(DATA_PATH / filename, chunksize=50_000, encoding="utf-8"):
            yield chunk
    return read_data


@dlt.source
def spotify_csv():
    return[
        csv_resource("tracks", "tracks.csv"),
        csv_resource("dataset", "dataset.csv"),
        csv_resource("artists", "artists.csv"),
    ]

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="musicquiz",
        destination=dlt.destinations.duckdb("duckdb/warehouse.duckdb"),
        dataset_name="raw"
    )
    print(pipeline.run(spotify_csv(), loader_file_format="parquet"))