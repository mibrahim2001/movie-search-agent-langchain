from langchain_community.tools import DuckDuckGoSearchResults, YouTubeSearchTool
from langchain_core.tools import Tool
from typing import List, Optional
from langchain_google_community import GoogleSearchAPIWrapper
import os

class SearchToolKit:
    """A toolkit that provides various search-related tools."""
    
    def __init__(self):
        """Initialize the search toolkit with DuckDuckGo, YouTube, and Google search capabilities."""
        self.ddg_search = DuckDuckGoSearchResults(name="DuckDuckGo_Search")
        self.youtube_search = YouTubeSearchTool(name="YouTube_Search")
        self.google_search: Optional[Tool] = None

        try:
            self._google_wrapper = GoogleSearchAPIWrapper()
            self.google_search = Tool(
                name="Google_Search",
                description="Search Google for recent results.",
                func=self._google_wrapper.run,
            )
        except Exception as e:
            print(f"Failed to initialize Google Search: {str(e)}")

    def get_tools(self) -> List[Tool]:
        """Get all available search tools.
        
        Returns:
            List[Tool]: List of available search tools
        """
        tools = [self.youtube_search]
        if self.google_search:
            tools.append(self.google_search)
        return tools
