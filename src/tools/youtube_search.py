from langchain_community.tools import YouTubeSearchTool
from langchain_core.tools import tool

@tool
def search_youtube(query: str, num_results: int = 1) -> str:
    """Search YouTube for videos and return relevant results.

    Args:
        query (str): The search query for finding YouTube videos (title, channel, or topic)
        num_results (int, optional): Number of results to return. Defaults to 1.

    Returns:
        str: Video results urls.
    """
    youtube_search = YouTubeSearchTool()
    return youtube_search.run(query, num_results)
