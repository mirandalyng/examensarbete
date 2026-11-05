
# Samtal med Kokchun 05/11

Projekt: musikquiz-app med filtrering och AI-agent (examensarbete, Data Engineer)

## 1. Arkitektur: så hänger det ihop

1. **Hela databasen embeddas.** Varje låt (rad) får en egen vektor, som lagras tillsammans med sin metadata (artist, album, genre, år osv.).
2. **Användaren filtrerar** (t.ex. år och genre) och ett **subset** av låtar blir kvar. Varje låt i subsetet har redan sin vektor, så vektorsök kan göras *inom* det filtrerade urvalet.
3. **Agenten väljer ut ett litet antal låtar** (t.ex. 5) som följdfrågorna ska baseras på. Här kommer `output_type` in. Tolkning: agentens svar ska ha en strikt, strukturerad form (t.ex. en Pydantic-modell med en lista av låtar) så att formatet går att lita på. *Bekräfta tolkningen med läraren.*
4. **LLM:en får ett verktyg (tool).** Den ska inte ha hela databasen i prompten, utan anropa en funktion som söker och hämtar rader.
5. **LLM:en kopplas till vektordatabasen** (LanceDB eller DuckDB) via det verktyget, så att den själv kan plocka ut låtar.

```
Användare → filter (år, genre) → subset med vektorer
                                      ↓
                  LLM ←→ verktyg (sök i databasen)
                                      ↓
                  output_type: t.ex. 5 låtar → quiz + följdfrågor + facit
```

## 2. Öppen fråga: DuckDB eller LanceDB?

Läraren föreslog att **använda DuckDBs vektorsök i stället för LanceDB**. Frågor att reda ut:

- Hur går man från DuckDB till LanceDB?
- Hur kopierar man över datan?
- Är det värt det?

### Hur det går till tekniskt

LanceDB kan skapa en tabell direkt från Arrow, pandas eller parquet. Två vägar:

- Läs in **parquet-exporten** från marten.
- Hämta från DuckDB som Arrow och skicka in i LanceDB:

```python
import duckdb, lancedb

con = duckdb.connect("music.duckdb")
arrow_table = con.sql("SELECT * FROM mart_songs").arrow()

db = lancedb.connect("./lancedb")
table = db.create_table("songs", data=arrow_table)
```

Själva kopieringen är litet jobb. Det som kräver arbete är att **generera embeddings** och att **hålla DuckDB och LanceDB synkade** om datan ändras.

### Är det värt det?

| | DuckDB | LanceDB |
|---|---|---|
| Pipeline | Ingen ny komponent | Extra steg och extra komponent att deploya |
| Filtrering + vektorsök | En SQL-fråga | Metadatafilter + vektorsök i samma anrop |
| Inlärning | Redan känt | Lärs ut nästa vecka |
| Rapportvärde | Enklare | Tydlig jämförelse att motivera |

### Rekommendation

Bygg verktyget mot ett **tydligt gränssnitt**: en funktion som tar filter och returnerar låtar. Då kan backend bytas utan att agenten ändras. Börja med DuckDB, prova LanceDB när ni lärt er det, och **dokumentera jämförelsen i rapporten** (visar metodmedvetenhet och kritisk reflektion, vilket krävs för VG).

## 3. Optimering av tokens och kvalitet

### TOON (Token-Oriented Object Notation)

- Kompakt format för att skicka strukturerad data till en LLM.
- Särskilt bra för listor med likadana objekt, som låtrader, där JSON upprepar nyckelnamnen för varje rad.
- Kan spara tokens när verktyget returnerar t.ex. 20 låtar.
- **Mät själva:** JSON vs TOON, antal tokens och svarskvalitet. Ger ett konkret resultat till rapporten.

### Thinking

- Slå på/ställ in thinking (resonemang) hos modellen.
- Obs: thinking kostar normalt *fler* tokens, inte färre. Vinsten är oftast bättre resultat, t.ex. bättre planering av verktygsanrop och färre felaktiga försök, vilket kan spara tokens totalt.
- **Testa med och utan** och jämför, så blir det ett underbyggt val.

## 4. Saker att kolla

- **Vad embeddas egentligen?** Datasetet har mest numeriska audio features, medan embeddings oftast görs på text. Bygg troligen en textbeskrivning per låt (artist, låttitel, genre, mood härlett från valence/energy) och embedda den.
- **Årtal saknas i datasetet.** `dataset.csv` har inget släppår, men ni vill filtrera på år och ställa följdfrågor om släppår och album. Har datan berikats via API i pipelinen? Annars måste det lösas, eftersom det är kärnan i filtret.
- **Bekräfta `output_type`-tolkningen** med läraren.

## 5. Att-göra

- [ ] Bestäm vad som ska embeddas och bygg textbeskrivning per låt
- [ ] Lös släppår/album-berikning av datan
- [ ] Definiera verktygsfunktionen (filter in, låtar ut) oberoende av backend
- [ ] Definiera `output_type` (t.ex. Pydantic-modell)
- [ ] Prova DuckDB vektorsök och, efter nästa veckas lektion, LanceDB
- [ ] Jämför JSON vs TOON samt med/utan thinking och skriv in i rapporten