from duckduckgo_search import DDGS


def get_live_news_context(sport_name):
    """
    Searches the live web for recent sport news, matches, or events.
    Returns a unified text summary of search snippets.
    """
    search_query = f"{sport_name} latest tournament results championship winners news 2026"
    retrieved_texts = []

    print(f"Executing web search for: '{search_query}'...")
    try:
        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=3)

            for index, r in enumerate(results, start=1):
                title = r.get("title", "No Title")
                snippet = r.get("body", "No Snippet Content Available")
                retrieved_texts.append(f"Web Source {index}: {title}\nSnippet: {snippet}")

    except Exception as e:
        print(f"Web search failed or fell back: {e}")
        return "No recent search engine updates available due to a connectivity issue."

    if not retrieved_texts:
        return "No relevant live web results were found."

    return "\n\n".join(retrieved_texts)
