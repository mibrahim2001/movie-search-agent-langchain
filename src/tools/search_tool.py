from langchain_community.tools import DuckDuckGoSearchResults
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from typing import Literal
import os

class SearchTool:
    def __init__(self, preferred_engine: Literal["google", "duckduckgo"] = "google"):
        """Initialize search tool with preferred engine.
        
        Args:
            preferred_engine: The preferred search engine to use ("google" or "duckduckgo").
                            If Google credentials are not available and Google is preferred,
                            it will fallback to DuckDuckGo.
        """
        # Check if Google is available when it's preferred
        if preferred_engine == "google" and not (os.getenv('GOOGLE_API_KEY') and os.getenv('GOOGLE_CSE_ID')):
            print("Google API credentials not found. Falling back to DuckDuckGo.")
            self.search_engine = "duckduckgo"
        else:
            self.search_engine = preferred_engine
            
        self._setup_search_engine()

    def _setup_search_engine(self):
        if self.search_engine == "google":
            self.search = GoogleSearchAPIWrapper()
            self.search_func = self._google_search
        else:
            self.search = DuckDuckGoSearchResults()
            self.search_func = self._duckduckgo_search

    def _google_search(self, query: str):
        return self.search.results(query, 1)

    def _duckduckgo_search(self, query: str):
        return self.search.run(query)

    def get_search_tool(self) -> Tool:
        return Tool(
            name=f"{self.search_engine}_search",
            description=f"Search {self.search_engine.capitalize()} for recent results.",
            func=self.search_func
        )

    def switch_engine(self, engine: Literal["google", "duckduckgo"]):
        if engine == "google" and not (os.getenv('GOOGLE_API_KEY') and os.getenv('GOOGLE_CSE_ID')):
            raise ValueError("Google API credentials not found. Cannot switch to Google search.")
        self.search_engine = engine
        self._setup_search_engine()
