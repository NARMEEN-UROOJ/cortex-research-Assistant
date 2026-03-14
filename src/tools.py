from ddgs import DDGS

def search_web(query: str, max_results: int = 5) -> list:
    """Search the web using DuckDuckGo and return results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []

def format_search_results(results: list) -> str:
    """Format search results into readable text for agents."""
    if not results:
        return "No results found."
    
    formatted = ""
    for i, r in enumerate(results, 1):
        formatted += f"\n[{i}] {r.get('title', 'No title')}\n"
        formatted += f"    {r.get('body', 'No content')}\n"
        formatted += f"    Source: {r.get('href', 'No URL')}\n"
    
    return formatted