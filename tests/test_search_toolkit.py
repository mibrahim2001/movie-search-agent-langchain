from src.tools.search_tool_kit import SearchToolKit
from langchain_core.tools import Tool, BaseTool

def test_search_toolkit_initialization():
    """Test that SearchToolKit initializes with expected tools."""
    toolkit = SearchToolKit()
    
    # Test that we get a list of tools
    tools = toolkit.get_tools()
    assert isinstance(tools, list)
    assert len(tools) > 0
    
    # Test that all items are Tool or BaseTool instances
    assert all(isinstance(tool, (Tool, BaseTool)) for tool in tools)
    
    # Test that YouTube search tool is always present
    assert any(tool.name == "YouTube_Search" for tool in tools)

def test_google_search_results():
    """Test the Google search results formatting."""
    toolkit = SearchToolKit()
    
    # Skip test if Google Search is not initialized
    if not toolkit.google_search:
        return
        
    # Test that the function exists and returns expected type
    assert hasattr(toolkit, '_top5_google_results')
    try:
        results = toolkit._top5_google_results("test query")
        assert isinstance(results, list)
        assert len(results) <= 5  # Should return at most 5 results
    except ValueError:
        # This is expected if Google Search is not properly initialized
        pass 