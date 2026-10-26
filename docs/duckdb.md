# Projektlogg: raw-pipeline och datavalidering

## Vad som är gjort

1. **Beslut:** Snowflake ersattes av DuckDB. Motivering: liten datamängd (ca 114 000, 587 000 respektive ca 1 miljon rader), ingen kostnad, enklare deploy. Snowflake nämns som skalningsväg.
2. **Pipeline för raw (dlt → DuckDB):** `dlt/load_data.py` läser `tracks.csv`, `dataset.csv` och `artists.csv` och laddar dem orörda till schemat `raw` i `warehouse.duckdb` (projektets rotmapp).
3. **Felsökning:**
   - `ModuleNotFoundError: duckdb`: saknade `dlt[duckdb]`.
   - `FileNotFoundError`: relativ sökväg, skriptet måste köras från projektroten.
   - `OutOfMemoryException`: dlt:s standardformat `insert_values` skalar inte för stora CSV-filer. Lösning: `loader_file_format="parquet"`, yielda DataFrames och rensa `~/.dlt/pipelines/musicquiz` (dlt återupptog annars det trasiga paketet).
   - `Database file version 999`: Python-paketet `duckdb` (2.0.0) var nyare än CLI:n (1.4.1). Lösning: låsa `duckdb==1.4.1`.
4. **Datavalidering i UI:**
   - `dataset`: 114 000 rader, 89 741 unika `track_id` (samma låt ligger under flera genrer).
   - `tracks`: 586 672 rader, inga dubbletter.
   - Matchning på `track_id`: 17 002 låtar (18,9 %). Matchning på namn + första artist: 23 947 låtar.
   - Efter popularity ≥ 40 finns hundratals till tusentals låtar per årtionde från 60-talet till 10-talet. Före 1960 och efter 2021 är det tunt.
5. **Designbeslut (att dokumentera):**
   - `dataset` är bas, eftersom `tracks` saknar albumnamn.
   - Året hämtas via namn + artist (tidigaste året), deduplicering på namn + artist, popularity ≥ 40.
   - Årtal och genre är valfria filter. Agenten ska tala om när ett filter ger för få låtar.
   - Känd begränsning: artistnamn med komma, och två olika låtar med samma namn och artist.
6. **dbt:** mappstrukturen är skapad men tom. Fylls i tillsammans nästa dag.

## Installerat

```bash
uv add "dlt[duckdb]" pandas pyarrow
uv add "duckdb==1.4.1"
```

Att göra: `uv add dbt-duckdb`. Kontrollera efteråt att `duckdb` fortfarande är 1.4.1.

## Användbara kommandon

| Syfte | Kommando |
|---|---|
| Kör raw-pipelinen (från projektroten) | `uv run dlt/load_data.py` |
| Nollställ vid trasig dlt-körning | `rm -rf ~/.dlt/pipelines/musicquiz` och `rm -f warehouse.duckdb` |
| Öppna DuckDB UI | `duckdb -ui duckdb/warehouse.duckdb` |
| Lista alla tabeller | `duckdb warehouse.duckdb -c "show all tables"` |
| Kolla versioner | `duckdb --version` och `uv run python -c "import duckdb; print(duckdb.__version__)"` |
| Synka miljön efter `git pull` | `uv sync` |
| Testa dbt-konfigurationen | `cd dbt_project && uv run dbt debug --profiles-dir .` |
| Bygg modeller | `uv run dbt run --profiles-dir .` |
| Kör tester | `uv run dbt test --profiles-dir .` |

## Att komma ihåg

- Stäng DuckDB UI innan pipeline eller dbt körs, eftersom filen bara tillåter en skrivande process.
- `warehouse.duckdb` och `*.duckdb.wal` ska i `.gitignore`. Committa `pyproject.toml` och `uv.lock`.
- Flödet är `CSV → dlt → raw → dbt → staging → marts → LanceDB`.

## Nästa steg

1. Fyll i dbt-filerna (`dbt_project.yml`, `profiles.yml`, macro, `sources.yml`, tre modeller).
2. Kör `dbt debug`, `dbt run` och `dbt test`.
3. Kontrollera `pct_med_ar` och antal låtar per årtionde i `marts.quiz_tracks`.
4. Planera genremappning (114 → 15-20 huvudgenrer) och embedding-text för LanceDB.