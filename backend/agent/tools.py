import httpx

# Wikipedia's API address (English Wikipedia)
WIKI_API = "https://en.wikipedia.org/w/api.php"

# Wikipedia asks every client to identify itself with a User-Agent,
# otherwise the requests may be blocked
HEADERS = {
    "User-Agent": "music-quiz-examensarbete/1.0 (lyngmiranda@gmail.com)"}


async def search_wikipedia(query: str) -> str:
    """Search Wikipedia and return the text of the best matching article.
    Use it to find facts about an artist or a song. Include both names for
    songs, for example 'Dancing Queen ABBA song'. You can call it several
    times with different queries."""

    # Open an HTTP client that sends our headers with every request
    # and gives up after 15 seconds
    async with httpx.AsyncClient(headers=HEADERS, timeout=15) as client:

        # STEP 1: Search for articles that match the query.
        # srlimit=1 means we only want the best match.
        search = await client.get(WIKI_API, params={
            "action": "query", "list": "search", "srsearch": query,
            "srlimit": 1, "format": "json",
        })
        # Raise an error if Wikipedia answered with a failure (e.g. 500)
        search.raise_for_status()

        # Pull the list of hits out of the JSON response
        hits = search.json()["query"]["search"]

        # If nothing was found, tell the model so it can try another query
        if not hits:
            return "No results found."

        # STEP 2: Take the title of the best hit
        title = hits[0]["title"]

        # STEP 3: Fetch the article text for that title.
        # explaintext=1 gives plain text instead of HTML,
        # redirects=1 follows redirects to the real article.
        page = await client.get(WIKI_API, params={
            "action": "query", "prop": "extracts", "explaintext": 1,
            "titles": title, "redirects": 1, "format": "json",
        })
        page.raise_for_status()

        # The response contains pages keyed by an ID we don't know in advance,
        # so we take the first (and only) page and read its text
        pages = page.json()["query"]["pages"]
        text = next(iter(pages.values())).get("extract", "")

        # STEP 4: Return the title and the first 6000 characters.
        # We cut the text so the model doesn't receive a huge article
        # (long text is slow and costs more).
        return f"{title}\n\n{text[:8000]}"
