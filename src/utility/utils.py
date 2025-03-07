import os

def load_system_prompt():
    """Load the system prompt from the markdown file in the prompts directory."""
    # Get the src directory path (one level up from utility)
    src_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(src_dir, "prompts", "system_prompt.md")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip() 