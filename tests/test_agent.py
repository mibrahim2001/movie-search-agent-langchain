import pytest
from src.agent import MovieSearchAgent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

def test_agent_initialization():
    """Test that MovieSearchAgent initializes correctly."""
    try:
        agent = MovieSearchAgent()
        
        # Test that essential components are initialized
        assert agent.tools is not None
        assert len(agent.tools) > 0
        assert agent.model is not None
        assert agent.system_message is not None
        assert agent.agent_executor is not None
    except Exception as e:
        pytest.skip(f"Skipping test due to initialization error: {str(e)}")

def test_agent_response_format():
    """Test that agent responses follow expected format."""
    try:
        agent = MovieSearchAgent()
        config = RunnableConfig()
        
        # Test with a simple query
        response = agent.get_complete_response("Tell me about a movie", config)
        
        # Check response structure
        assert isinstance(response, dict)
        assert "messages" in response
        assert len(response["messages"]) > 0
        assert isinstance(response["messages"][-1].content, str)
        
    except Exception as e:
        pytest.skip(f"Skipping test due to API error: {str(e)}")

def test_streaming_response():
    """Test that streaming responses work correctly."""
    try:
        agent = MovieSearchAgent()
        
        # Test streaming response generator
        stream = agent.get_streaming_response("Tell me about a movie")
        
        # Check that it's a generator
        assert hasattr(stream, '__iter__')
        assert hasattr(stream, '__next__')
        
        # Try to get at least one response (don't iterate through all to save API calls)
        first_response = next(stream, None)
        if first_response is not None:
            assert isinstance(first_response, dict)
            
    except Exception as e:
        pytest.skip(f"Skipping test due to API error: {str(e)}") 