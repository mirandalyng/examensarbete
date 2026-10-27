## Här skriver vi vad som gjorts under dagen.

```md
Datum - Rubrik
Medverkande:
Beskrivning:
Information: - vilken fil du jobbat i - var finns ytterligare information - ex mapp/fil
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
