from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from tools.search_tool import SearchTool
from tools.youtube_search import youtube_search
import os

load_dotenv()  # Load environment variables from .env file

# Initialize search tools with preferred engine
search_tool = SearchTool(preferred_engine="duckduckgo").get_search_tool()


# print(search_tool.invoke("Orphan movie imdb rating"))

model = init_chat_model("gpt-4", model_provider="openai")
tools = [search_tool, youtube_search]

# Load system prompt from markdown file
def load_system_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.md")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()

system_message = load_system_prompt()
agent_executor = create_react_agent(model, tools, prompt=system_message)

for step in agent_executor.stream(
    {"messages": [HumanMessage(content="3 Idiots movie")]},
    stream_mode="values"
): step["messages"][-1].pretty_print()