from langchain_tavily import TavilySearch


def get_profile_url_tavily(name: str):
    """Searches for LinkedIn profile page specifically"""
    search = TavilySearch()
    query = f"{name} site:linkedin.com/in/"
    res = search.run(query)
    return res
