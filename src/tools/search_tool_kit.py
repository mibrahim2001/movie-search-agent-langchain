from langchain_community.tools import DuckDuckGoSearchResults, YouTubeSearchTool
from langchain_core.tools import Tool
from typing import List, Optional, Literal
from langchain_google_community import GoogleSearchAPIWrapper
import os

class SearchToolKit:
    """A toolkit that provides various search-related tools."""
    
    def __init__(self, search_preference: Literal["google", "duckduckgo"] = "duckduckgo"):
        """Initialize the search toolkit with the preferred search engine and YouTube search.
        
        Args:
            search_preference (str): Preferred search engine ("google" or "duckduckgo")
        """
        self.search_preference = search_preference.lower()
        self.ddg_search = None
        self.google_search = None
        
        # Initialize the preferred search engine
        if self.search_preference == "duckduckgo":
            self.ddg_search = DuckDuckGoSearchResults(name="DuckDuckGo_Search")
        elif self.search_preference == "google":
            try:
                self._google_wrapper = GoogleSearchAPIWrapper()
                self.google_search = Tool(
                    name="Google_Search",
                    description="Search Google for recent results.",
                    func=self._top5_google_results,
                )
            except Exception as e:
                print(f"Failed to initialize Google Search: {str(e)}")
                # Fallback to DuckDuckGo if Google fails
                self.search_preference = "duckduckgo"
                self.ddg_search = DuckDuckGoSearchResults(name="DuckDuckGo_Search")
        
        self.youtube_search = YouTubeSearchTool(name="YouTube_Search")
    
    def _top5_google_results(self, query: str) -> List[str]:
        """
        Fetch the top 5 Google search results for a given query.

        Args:
            query (str): The search query string.

        Returns:
            List[str]: A list of the top 5 search result snippets.
        """
        if not self.google_search:
            raise ValueError("Google Search is not initialized.")
        return self._google_wrapper.results(query, 5)
    
    def get_tools(self) -> List[Tool]:
        """Get available search tools based on the preferred search engine.
        
        Returns:
            List[Tool]: List of available search tools including YouTube and the preferred search engine
        """
        tools = [self.youtube_search]
        
        if self.search_preference == "google" and self.google_search:
            tools.append(self.google_search)
        elif self.search_preference == "duckduckgo" and self.ddg_search:
            tools.append(self.ddg_search)
            
        return tools

    
