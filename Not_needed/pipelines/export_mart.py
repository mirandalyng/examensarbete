import duckdb

with duckdb.connect("../duckdb/warehouse.duckdb") as conn:
    df = conn.sql("select * from marts.quiz_tracks;").df()

df.to_parquet("../data/serving/mart.parquet", index=False)
