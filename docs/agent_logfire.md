# Sammanfattning: vad vi ändrade för att koppla på Logfire

## Filer som ändrades eller skapades (`backend/`)

**`agent/prompts.py` (ny)**
- Konfigurerar Logfire en gång: `logfire.configure(variables=VariablesOptions())`. Nycklarna läses automatiskt från `.env`.
- Funktionen `get_prompt(name, default, label)` hämtar prompten från Logfire med ett namn och en label (nu `latest`). Hämtningen tvingas om varje gång (`refresh_sync(force=True)`), så vi får senaste versionen.
- Misslyckas hämtningen används `default`-texten tyst. Skrivs "music assistant" ut är det alltså ett tecken på att något är fel.

**`agent/agent.py` (ändrad)**
- Prompten ligger inte längre hårdkodad i filen. `instructions=get_prompt()` hämtar den från Logfire i stället.
- Ny funktion `track_context`, märkt med `@music_agent.instructions`. Den körs vid varje körning och lägger låtdatan från `MusicData` (låt, artist, album, år, genrer) i instruktionerna. Agenten utgår då från riktig data i stället för att gissa.
- Importerna är nu relativa (`from .deps import ...`, `from .prompts import ...`), så att det fungerar när vi kör från projektroten.

**`agent/deps.py` (ändrad)**
- `FollowUps` fick fältet `options` (tidigare `option`), som nu är valfritt (`list[str] | None = None`), så att inte alla frågor måste ha svarsalternativ.
- En validator kontrollerar att `correct_answer` finns bland `options`. Annars skickas ett felmeddelande tillbaka till modellen, som får göra ett nytt försök. Omförsöken syns i Logfire och är användbara som mätvärde.

**`playground/main.py` (ny, ersatte mappen `logfire/`)**
- Testskript som skapar en `MusicData` med en testlåt, kör `music_agent.run(prompt, deps=...)` och skriver ut resultatet.
- Anropar `logfire.instrument_pydantic_ai()`, som gör att körningar och modellanrop syns som spår i Logfire.
- Har inget eget `logfire.configure()`. Det finns redan i `prompts.py`, och två anrop skriver över varandra.

**`__init__.py` (nya, i `backend/agent/` och `backend/playground/`)**
- Behövs för att Python ska behandla mapparna som paket.

## Utanför koden

**`.env`**, två olika nycklar:
- `LOGFIRE_TOKEN` är en write-token som skickar spår.
- `LOGFIRE_API_KEY` är en API-nyckel med scopet `project:read_variables`, som läser prompterna.

**I Logfire (projektet coachy-quiz):**
1. Skapade prompten under Prompts och sparade den som v1.
2. Lade en label (`latest`) på prompten under Managed Variables. Utan label används default-texten.

## Så kör man det

Från projektroten, som modul:

```
uv run python -m backend.playground.main
```

## Saker som är bra att veta

- **Namnet i koden är inte samma som i Logfire.** Logfire lägger till prefixet `prompt__` på prompten, och koden gör det också (`f"prompt__{name}"`). Variabeln heter `prompt__prompt_music_agent_instructions` hos oss, så `name` i `prompts.py` är `"prompt_music_agent_instructions"`. Variabelns namn står under "Reference it from your code" på variabelns sida i Logfire.
- **Ny promptversion:** spara som v2, kontrollera att labeln pekar på den, och starta om skriptet.
- **Mappen får inte heta `logfire`,** eftersom den då kan krocka med det riktiga paketet.


# Nästa steg

1. **Skapa sökverktyget** (Wikipedia i `tools.py`) och koppla det till agenten med `tools=[...]`. Testa det först med en enda låt och titta i Logfire-spåret på om agenten faktiskt anropar verktyget och får tillbaka text.
2. **Lägg in verktygens namn i prompten** (`search_wikipedia`, `get_wikipedia_page`) och spara den som v2. Då vet modellen vad den ska använda.
3. **Jämför v1 och v2** på samma testlåtar. Kolla om facit stämmer mot källan, om frågorna blir roligare och hur ofta den faller tillbaka på metadata.

Skapa också en liten fast uppsättning testlåtar, till exempel 4-5 stycken med olika data (en känd artist, en obskyr, en med saknade fält, en med flera genrer). Då kommer skillnaderna i Logfire från prompten och inte från att datan varierar.

