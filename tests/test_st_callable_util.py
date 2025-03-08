import pytest
from utility.st_callable_util import get_streamlit_cb
from streamlit.delta_generator import DeltaGenerator
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_container():
    """Create a mock Streamlit container for testing."""
    container = MagicMock(spec=DeltaGenerator)
    container.container.return_value = MagicMock(spec=DeltaGenerator)
    container.empty.return_value = MagicMock(spec=DeltaGenerator)
    return container

def test_streamlit_cb_creation(mock_container):
    """Test that Streamlit callback handler is created correctly."""
    cb = get_streamlit_cb(mock_container)
    
    # Test that callback handler has required methods
    assert hasattr(cb, 'on_llm_new_token')
    assert hasattr(cb, 'on_tool_start')
    assert hasattr(cb, 'on_tool_end')

def test_on_llm_new_token(mock_container):
    """Test token streaming behavior."""
    cb = get_streamlit_cb(mock_container)
    
    # Test token handling
    test_token = "test"
    cb.on_llm_new_token(test_token)
    
    # Verify that write was called on the token placeholder
    cb.token_placeholder.write.assert_called_once()

@patch('streamlit.empty')
@patch('streamlit.write')
@patch('streamlit.code')
@patch('streamlit.status')
def test_on_tool_start(mock_status, mock_code, mock_write, mock_empty, mock_container):
    """Test tool start handling."""
    cb = get_streamlit_cb(mock_container)
    
    # Mock the status context manager
    mock_status_ctx = MagicMock()
    mock_status.return_value = mock_status_ctx
    mock_status_ctx.__enter__.return_value = mock_status_ctx
    
    # Test tool start event
    serialized = {"name": "test_tool"}
    input_str = "test input"
    
    cb.on_tool_start(serialized, input_str)
    
    # Verify that the container was used
    assert cb.thoughts_placeholder is not None
    
def test_on_tool_end(mock_container):
    """Test tool end handling."""
    cb = get_streamlit_cb(mock_container)
    
    # Create a mock output
    class MockOutput:
        content = "test output"
    
    # Set up the tool output placeholder
    cb.tool_output_placeholder = MagicMock(spec=DeltaGenerator)
    
    # Test tool end event
    cb.on_tool_end(MockOutput())
    
    # Verify that code was called on the output placeholder
    cb.tool_output_placeholder.code.assert_called_once_with("test output") 