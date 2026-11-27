## Här skriver vi vad som gjorts under dagen.

```md
### Datum - Rubrik

#### Medverkande:

#### Beskrivning:

#### Information: - vilken fil du jobbat i - var finns ytterligare information - ex mapp/fil
```

### 6/10 - Setup av github projects och gruppkontakt

#### Medverkande:

Lisa, Miranda och Rickard

#### Beskrivning:

- Skapat repo och testat att det funkar för alla
- Satt upp github projects och skapat issues
- Bestämt git-regler
- Skrivit gruppkontrakt
- Påbörjat projektstuktur (mappar och filer)
- Lagt till git_commands.md

#### Information:

- Repo (vsc)
- Github projects

---

### 12/10 "Hämta data och göra eda"

#### Medverkande: Lisa, Rickard, Miranda

#### Beskrivning:

Vi hämtade data från Kaggle (Spotify) och Musicbrainz (API). Otydliga regler om vi får använda Deezers API för att spela upp låtar men vi har mailat dom och inväntar svar. Det vi kan göra är att använda Spotify för att spela upp låtar men då behövs "track_id" som saknas i API:et för Musicbrainz. Vi avvaktar tills vi får svar från Deezer men testar använda Kaggledatan och får kanske nöja oss med det sålänge. mer värt att lägga tid på AI-agenten än att hitta mer data?

Vi testade sedan koppla endast kaggle datan (track id ) mot spotify url för att få ut en url för varje låt baserat på tack_id i kaggle-dataset. Detta fungerade bra!

#### Information:

- Kolla gärna igenom eda för Kaggle och Musicbrainz.

- Kör en uv sync

- Ladda ner dataset (Discord) eller länk: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset och skapa en mapp data/raw. Lägg dataset i raw-mappen.

---

### 26/10 "Byggt staging-lagret"

#### Medverkande: Rickard, Miranda, Lisa

#### Beskrivning:

- Byggt staging-modeller i dbt för artists, tracks och albums.
- Byggt mellantabellen stg_track_artists, som kopplar ihop låtar och artister.
  En låt kan ha flera artister, så id_artists i tracks delas upp till en rad per artist.
- Kontrollerat kopplingen mellan tracks och artists: ca 20 000 artistkopplingar saknas
  i artists.csv, men bland låtar med popularitet ≥ 50 berörs bara 440 (0,6 %).

---

### 27/10 "Fortsätter med staging & mart"

#### Medverkande: Rickard, Miranda, Lisa

#### Beskrivning:

**Staging:**

- Städning:
  Städar tabellerna med (trim, max, coalesce)
  tar endast med icke-nulla värden

**Mart:**

- **Rensar bort tecken:**
  Tar bestlutet om att ta bort andra bokstäver än latinska.
  Rensar bort tecken (ex koreanska, kinesiska) då detta blir svåra att tolka för en användare som inte kan språket.
  Detta görs i Mart då det är ett beslut om att inte behålla dessa.

- **Popularity:**
  - artist : > 50 and tracks > 20
  - tracks: > 50 and artist > 20

  Detta görs för att inte helt okända låtar och artister ska komma med i datan. Baserat på EDA och duckkdb - research innehåller datan extremt mycket mindre och okända artister/låtar.

- **Join:**
  Joinar samtliga staging-modeller till ett OBT (one big table) som ska användas för att visas i dashboarden.

- **Seeds:**
  Grupperar våra genres då dessa innehåller många sub- och mindre genre. Det är ett val vi gjort då AI-agenten och användaren inte ska behöva kunna dessa mindre genres för att få låtar som kan tillhöra dessa.

  I seed filen ingår också priority för att den ska veta var den ska grupperas ihop med.

  Vi väljer att endast ha kvar main_genre som genre

#### Information

**OM uppdateringar gjorts!**
Kör om pipelinen:
uv run dlt/load_data.py

Kör dbt - filera

uv run dbt --select {model_name}

kör seed:
dbt seed

---

### 3/11 - 26 - Updating Mart, dbt-testing. Filter för genre, årtionde

#### Medverkande: Lisa, Rickard, Miranda

#### Beskrivning:

- gjort ett dokument för källor (sources.md)

  **Mart**

- popularity 50-30
- Release year >= 1950
- lagt till kolumn 'decade'

**Dbt-testing**

- Tester för unique och not null
- Relationships i track_artists

**Filters**

- årtionde
- genre

**Randomize**

- randomize låtar baserat på filterad dataframe från årtione och genre

**Antal låtar**

- antal låtar som användaren vill ha
- här läses random, filter årtionde och filter genre in

#### Information: - vilken fil du jobbat i - var finns ytterligare information - ex mapp/fil

- backend/filters
- dbt/models/mart

ps: kör uv sync och kör om dbt filerna med 'uv run dbt run'

---

### 5 nov - Testing with vector embedding in lanceDB

#### Medverkande: Miranda

#### Beskrivning:

- Testade quick setup från lanceDB dokumentation
- sentence-transformers används som provider för att skapa vector embeddings
- lancedb databas skapas
- test med ai - hjälp för att se om den kan hitta med hjälp av vector - sökning

#### Information:

- I mappen eda ligger en lance_db mapp.

---

### 6/11 - Skapa vektor embedding i Lancedb

#### Medverkande: Lisa, Rickard, Miranda

#### Beskrivning:

- Testat skapa vektor embeddings med våran data i ipynb först och sedan i .py
- Börja testa streamlit med datan
- Ändrat så att artist id inte tar med dubletter, samt tar bort låttitlar som har med 'Remasterd' då det ger felaktiga dubletter
- Möte med Kokchun

#### Information: -

- eda/lance_db
- backend/lancedb_connect.py

#### To Do / Nästa steg

- Performance (varför tar det så långt tid, dock kanske testa api först)
- API - endpoints osv med fastAPI för att separera frond-och-backend
- Börja med Agenten och Vector-sök (som ett verktyg) / RAG

- OPTIMERING: polars/ pandas + duckdb?

#### Fråga till gruppen: fritext eller bara filter?

- Vektorerna i `quiz`-tabellen används bara om användaren kan skriva fritext, t.ex. "hårdrock" eller "glad sommarmusik", och agenten söker med ett verktyg (`search_tracks`).
- Bygger vi inte fritext används de inte till något. Filtren behöver dem inte, och följdfrågorna med Wikipedia behöver egna vektorer i en annan tabell.
- Med nuvarande `search_text` (titel, artist, genre, album) fungerar sök på genre och namn, inte på stämning. För "glad" eller "lugn" behöver vi `valence`/`energy` från tracks.csv som ord i `search_text`.
- Fritext står i dag under "Vad är inte MVP" i projektplanen.
- Beslut behövs: ska fritext med i MVP, senare, eller inte alls?

### 10/11 ""

#### Medverkande: Lisa, Rickard, Miranda

#### Beskrivning:

- Flyttade frontend-filer til backend och ändrat sökvägar för att det ska fungera i streamlit

#### Information:

- i app.py i frontend ska ALLA importer och dess kommentarer till behållas för att sökvägen ska fungera. Denna ordning måste vara så. Den ändrar orning utan kommentarerna.

---

### 10/11 - städning i marten och repo, skapa endpoint och testa i Swagger UI, bygga funktioner och testa filtrering i frontend (streamlit)

#### Medverkande: Miranda, Rickard, Lisa

#### Beskrivning:

##### Mart:

- filtrering/städning i marten - ta bort remixer, live-versioner, dubbletter i track_name
- kasta låtar med genre 'other'

##### Städning i repo:

- flytta om mappar och ändra sökvägar

##### Skapa endpoint och testa i fastapi (swagger UI)

- i backend/api.py - skapat get endpoint för filtrering av genres, årtionden och antal låtar (med randomize)

##### Frontend

- skapa funktion för att testa filter i streamlit med requests

#### Information:

##### För att köra om mart - parquet-filen och lancedb:

```bash
cd dbt
uv run dbt run
cd piplines
uv run export_mart.py
cd backend
uv run lancedb_conn_vectorembeddings.py
uv run load_lancedb.py
```

##### För att testa i swagger ui:

```bash
cd backend
uv run uvicorn api:app --reload
```

##### För att testa i streamlit:

```bash
cd frontend
uv run streamlit run app.py
```

---

### 11/11 - Påbörja AI-agent, endpoint för att generera quiz med följdfrågor och testa i swagger och streamlit

#### Medverkande: Lisa, Miranda, Rickard

#### Beskrivning:

- Börjat skapa en ai-agent med enklare prompt för att se om den kan ta fram följdfrågor baserat på subsetet.
- skapat basemodel (classes) för struktured output
- testat i fronend och swagger ui

#### Information:

- backen/agent
- backend/api
- fronend/app

#### Todo:

- utforska sök på internet för agenten (just nu söker den bara baserat på metadatan (ibland internet) i subsetet vilket inte är korrekt)
- classes ? Är dessa rätt utformade ?
- dataclasses
- Multiagent delegation ?
- Skapa tools och promts
- Testa i logfire
- Följdfrågorna som genereras:
  - inte använda metadatan
  - endast årtal , artist?

---

### 13/11 - Logfire

#### Medverkande: Lisa 

#### Beskrivning: 
- skapade projekt i logfire 
- uppdaterade agent.py, deps.py och prompt.py för att testa prompts i logfire
- testade prompt i playground/main.py 

#### Information: - vilken fil du jobbat i - var finns ytterligare information - ex mapp/fil
- från logfire: en api-nyckel och en write-token (till .env)
- för mer info: se agent_logfire.md i docs
- för att kolla att rätt prompt används:
```bash 
cd backend && uv run python -c "from agent.prompts import get_prompt; print(get_prompt())"
```
--- 

### 13/11 - Ändring i /generated_quiz (api.py)

#### Medverkande: Miranda

#### Beskrivning:
- Tidigare: Sorterade låtarna på popularitet (track_popularity + artist_popularity), valde den populäraste halvan och körde agenten på en låt i taget med for och await. Svaret innehöll även answer_artist och answer_track.
- Nu: Alla låtar skickas till agenten samtidigt med asyncio.gather. Inget urval på popularitet görs, och svaret innehåller bara följdfrågan (result.output.model_dump()).
- Obs: Frontend matchar frågor och låtar via zip(tracks, followups), vilket fungerar eftersom gather behåller ordningen.

#### Att göra: Begränsa antalet samtidiga anrop med en semafor, eftersom Wikipedia-sökningarna gör varje anrop långsammare.

---
### 13/11 - Testa wikipedia api för följdfrågor

#### Medverkande: Rickard

#### Beskrivning:
- Testade ifall agenten kan skriva frågor utifrån riktig fakta istället för låtens metadata.
- Hämtade artistens wikipedia-sammanfattning i koden och skickade texten till agenten i prompten.

---

### 17/11 - Logfire (funkar för alla) - agent + tool flr wikipedia

#### Medverkande: Lisa, Miranda, Rickard

- Bytt till duckdb från parquet
- Logfire: Fixade 401-felen. Appen använde fel token, och prompten hämtades inte eftersom variabelnamnet inte matchade och v1 inte var släppt till labeln latest. Prompten läses nu från Logfire (variabel prompt__music_agent_instructions).

- Agent: La till ett Wikipedia-verktyg (search_wikipedia i tools.py) så att agenten kan söka fakta innan den skriver en följdfråga. Det registreras via tools=[search_wikipedia] i agent.py.

- Prompt: Ny prompt med roll, process (sök, välj ett bekräftat faktum, skriv frågan) och regler. Exakt 4 alternativ, aldrig artistnamn eller låttitel i frågan, svenska, fallback till metadata om inget hittas.

- Påbörjat README och städat i projektet (lagt filer vi ej använder i 'Not_needed')

---

### 24/11 - Testa prompts

#### Medverkande: Lisa, Miranda, Rickard

#### Beskrivning:
- Vi testade två olika prompts och jämförde dem i logfire
- Kontrollerade att alla regler följdes

#### Todo:
- Öka popularitet på både artist och låt
- Fortsätta testa prompts
- Definera vilka cases och dataclasses vi ska använda till LLM Judge


### Datum - Rubrik

#### Medverkande:

#### Beskrivning:
- **I marten:**
  - primary_artist för agentens sökning på wikipedia 
  - artist_list ger agenten hela bilden för sammarbeten osv men ställer inte till det i sökningen. 
  - höjt popularity till 60/40 för att minska antalet okända låtar. 
(kollat antal låtar och per genre/årtionde i duckdb ui (66127 låtar kvar))

**för agenten**
- backend/agent/deps.py 
  - uppdaterat class Musicdata (lagt till primary_artist, artist_list och title_normalized)
  - uppdaterat FollowUps:
    - source_title: str # Wikipedia-article title, or "metadata"
    - source_fact: str # lines that confirm the answerr
    - used_fallback: bool # True if the question is from the 'metadata'
  - model_validator för check av följdfrågor och options
- frontend/app.py
  - ändrat namn i frontend från artist_names till artist_list - artist_names finns inte längre men används i marten
- agent.py
  - uppdaterat music_agent_instructions så att agenten vet vad vi räknar som populär/känd och snyggare formatering 


#### Information: - vilken fil du jobbat i - var finns ytterligare information - ex mapp/fil

#### Todo:
- kör uv run dbt run --select quiz_tracks för att köra om marten
