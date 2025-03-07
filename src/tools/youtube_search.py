from langchain_community.tools import YouTubeSearchTool
from langchain_core.tools import tool

@tool
def search_youtube(query: str, num_results: int = 1) -> str:
    """Search YouTube for videos. Returns video titles and URLs."""
    youtube_search = YouTubeSearchTool()
    return youtube_search.run(query, num_results)
