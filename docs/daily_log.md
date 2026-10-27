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
