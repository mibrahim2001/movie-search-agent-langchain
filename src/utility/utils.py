import os
import uuid
from datetime import datetime

def load_system_prompt():
    """Load the system prompt from the markdown file in the prompts directory."""
    # Get the src directory path (one level up from utility)
    src_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(src_dir, "prompts", "system_prompt.md")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read().strip()
        return prompt.format(date=datetime.now().strftime("%Y-%m-%d"))

def generate_thread_id():
    """Generate a unique thread ID for chat sessions."""
    return f"thread_{uuid.uuid4().hex[:8]}" 