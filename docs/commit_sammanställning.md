# Sammanställning av Examensarbete

Detta dokument sammanfattar den kronologiska utvecklingen av examensarbetet baserat på projektets commit-historik och milstolpar.

---

## 1. Projektstart & Grundläggande Setup
* **Dokumentation & Struktur:** 
  * Projektet initierades och initial Git-dokumentation lades till (`lisas-test`).
  * Mappstruktur sattes upp och `.gitignore` konfigurerades (inklusive ignorering av `dlt`-hemligheter och DuckDB-filer).
* **Miljö & Verktyg:** 
  * Projektmiljön initierades med pakethanteraren `uv`.
  * Centrala beroenden installeras: `dotenv`, `ipykernel`, `matplotlib` och `requests`.
  * Löpande dokumentation startades via `daily_log`.

---

## 2. Utforskning av Datakällor & Initial EDA
* **MusicBrainz:** 
  * API-anrop testades och utvärdering genomfördes mot MusicBrainz datamängd.
* **Kaggle-dataset:** 
  * Beslut togs att importera ett större dataset från Kaggle (placerat i `data/raw`).
* **Datastädning:** 
  * Exploratory Data Analysis (EDA) genomfördes på Kaggle-datan.
  * Validering och datatvätt utfördes på `artist.csv` och `tracks.csv`.

---

## 3. Spotify-integration & Visualisering
* **URL-generering:** 
  * Utveckling av funktionalitet för att skapa direktlänkar till Spotify utifrån datasetets `track_id`.
* **Förhandsvisning:** 
  * EDA för Spotify-länkar och förhandsvisningar (embed previews).
  * Anteckningar och dokumentation om embed-integration uppdaterades.

---

## 4. Datamodellering & Databasmiljö (dbt, DuckDB & LanceDB)
* **Vektordatabas & Data Pipeline:** 
  * Setup och dokumentation för **LanceDB** initierades.
  * **DuckDB** testades tillsammans med data loading tool (`dlt`).
* **dbt-modellering:** 
  * Byggnation av datamodell via `dbt` med `.yml`-konfigurationer och SQL-frågor integrerade från DuckDB UI.
  * **Staging-lager:** Skapande av staging-tabeller (`stg_artists`, `stg_albums`, `stg_tracks`, `stg_track_artists`).
  * **Logik & Seeds:** Skapande av makron för listhantering samt seeds för genrer.

---

## 5. Marts, Datakvalitet & Logik för Quiz
* **Marts (Datamart-skikt):** 
  * Byggnation av `mart quiz_tracks` inklusive popularitetsindex per artist/track, unika artist-ID:n och Spotify-URL:er.
* **Datatvätt & Filtrering:** 
  * Rensning av titlar (t.ex. filtrering av "Remastered" för att förhindra felaktiga dubletter).
  * Implementation av makron för latinska språk och tecken.
  * Logik för filtrering baserat på årtionden (decades) och genrer.
* **Datatestning:** 
  * Implementation av dbt-tester (`not_null`, `unique`).

---

## 6. Vektorembeddings (LanceDB)
* **Vektoranalys:** 
  * Tester i EDA-miljö av LanceDB med mock-data, vektor-embeddings och embedding providers.
* **Integrering:** 
  * Implementation av vektorembeddings verifierades mot det transformerade datasetet.

---

## 7. Applikationsutveckling & Arkitektur (API & Frontend)
* **Backend & Webbygge:** 
  * Beroenden för webb- och API-ramverk lades till: `fastapi`, `uvicorn` och `streamlit`.
* **Quiz-logik:** 
  * Skript för slumpmässigt urval av låtar baserat på filtrerade dataframes och antalsfunktioner.
* **FastAPI Endpoints:** 
  * Skapande av endpoints för låtar och filter, vilka testades via Swagger UI.
* **Streamlit UI:** 
  * Frontend-bygge påbörjades med prestandaoptimeringar (snabbare sökning, korrekta anslutningsvägar via `lancedb_conn.py` och refaktorering till `backend/`).

---

## 8. Senaste Justeringar & Framtida Steg
* **Refaktorering:** Refaktorering av sökvektorer och korrigering av filvägar.
* **Mart-justeringar:** Justering av filtreringslogik i datamart.
* **Loggning:** Dokumentation och uppdatering av `daily_log`.