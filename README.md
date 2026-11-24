# examensarbete

## Short description and developers

## Techstack

## Project structure (tree - Miranda fixes)

### Setup:
#### Step 1 - clone repository and install dependencies
```bash
git clone https://github.com/mirandalyng/examensarbete.git
uv sync
```

#### Step 2 - Fetch data from kaggle
- create a folder in root named *data* and inside of *data* create a folder called *raw*

[Tracks and artists](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks?select=tracks.csv)
[Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)

#### Step 3 - run necessary files
1. fetches data from raw and loads it in to duckdb in parquet format

```bash
cd dlt
uv run load_data.py
```

2. dbt - transforms the data 
Before you can run dbt you need to:
- setup profiles.yaml # see profiles_example.yaml

```bash 
cd dbt
uv run dbt deps # to install dependencies/packages
uv run dbt run 
# use uv run dbt run --select <filename> to run one file at a time
```


#### To explore raw data and mart in duckdb ui
```bash
duckdb -ui duckdb/warehouse.duckdb
```

## Setup agent 
1. create an account at Nvidia (or something else) and paste you api key into .env
- see example.env

## Test locally 
#### Test backend (swagger ui)
```bash
cd backend
uv run uvicorn api:app --reload
```

#### Test frontend (streamlit)
*Note: Swagger ui needs to be running for streamlit to work*
```bash
cd frontend
uv run streamlit run app.py
```

### Want to explore more?
- logifre


### To read more about duckdb/logfire/etc 
- links to seperate documents here