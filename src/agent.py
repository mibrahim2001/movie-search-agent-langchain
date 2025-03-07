from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from tools.search_tool_kit import SearchToolKit
from utility import load_system_prompt
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()  # Load environment variables from .env file

# Initialize search toolkit
memory = MemorySaver()
config = {"configurable": {"thread_id": "abc123"}}
search_toolkit = SearchToolKit()
tools = search_toolkit.get_tools()

model = init_chat_model("gpt-4o-mini", model_provider="openai")
system_message = load_system_prompt()
agent_executor = create_react_agent(model, tools, prompt=system_message, checkpointer=memory)

for step in agent_executor.stream(
    {"messages": [HumanMessage(content="Top gun movie")]},
    stream_mode="values",
    config=config
): step["messages"][-1].pretty_print()