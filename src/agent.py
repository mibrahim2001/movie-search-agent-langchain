from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from tools import SearchTool, search_youtube
from utility import load_system_prompt
import os

load_dotenv()  # Load environment variables from .env file

# Initialize search tools with preferred engine
search_tool = SearchTool(preferred_engine="duckduckgo").get_search_tool()

model = init_chat_model("gpt-4", model_provider="openai")
tools = [search_tool, search_youtube]


system_message = load_system_prompt()
agent_executor = create_react_agent(model, tools, prompt=system_message, verbose=True)

for step in agent_executor.stream(
    {"messages": [HumanMessage(content="3 Idiots movie")]},
    stream_mode="values"
): step["messages"][-1].pretty_print()