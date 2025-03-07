from langchain_community.tools import DuckDuckGoSearchResults, YouTubeSearchTool
from langchain_core.tools import tool
from typing import List, Callable



class SearchToolKit:
    """A toolkit that provides various search-related tools."""
    
    def __init__(self):
        """Initialize the search toolkit with DuckDuckGo and YouTube search capabilities."""
        self.ddg_search = DuckDuckGoSearchResults(name="search_duckduckgo")
        self.youtube_search = YouTubeSearchTool(name="search_youtube")


    def get_tools(self) -> List[Callable]:
        """Get all available search tools.
        
        Returns:
            List[Callable]: List of available search tool functions
        """
        return [self.ddg_search, self.youtube_search]
