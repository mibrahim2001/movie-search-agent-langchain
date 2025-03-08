from src.utility.utils import load_system_prompt, generate_thread_id

def test_load_system_prompt():
    """Test that system prompt can be loaded successfully."""
    # Test that the function returns a non-empty string
    prompt = load_system_prompt()
    assert isinstance(prompt, str)
    assert len(prompt) > 0

def test_generate_thread_id():
    """Test thread ID generation."""
    # Test format and uniqueness
    thread_id1 = generate_thread_id()
    thread_id2 = generate_thread_id()
    
    # Check format
    assert thread_id1.startswith("thread_")
    assert len(thread_id1) == 15  # "thread_" (7 chars) + 8 hex chars
    
    # Check uniqueness
    assert thread_id1 != thread_id2
    
    # Check that the ID only contains valid characters
    hex_part = thread_id1[7:]  # after "thread_"
    assert all(c in '0123456789abcdef' for c in hex_part) 