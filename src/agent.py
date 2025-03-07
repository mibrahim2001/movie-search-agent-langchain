from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from tools.search_tool_kit import SearchToolKit
from utility import load_system_prompt
from langgraph.checkpoint.memory import MemorySaver
from typing import Generator, Dict, Any

class MovieSearchAgent:
    def __init__(self, model_name: str = "gpt-4o-mini", model_provider: str = "openai"):
        load_dotenv()
        
        # Initialize components
        self.memory = MemorySaver()
        self.config = {"configurable": {"thread_id": "abc123"}}
        self.search_toolkit = SearchToolKit()
        self.tools = self.search_toolkit.get_tools()
        
        # Initialize model and agent
        self.model = init_chat_model(model_name, model_provider=model_provider)
        self.system_message = load_system_prompt()
        self.agent_executor = create_react_agent(
            self.model,
            self.tools,
            prompt=self.system_message,
            checkpointer=self.memory
        )

    def get_response(self, user_input: str) -> Generator[Dict[str, Any], None, None]:
        """
        Get streaming response from the agent for a given user input.
        
        Args:
            user_input (str): The user's input message
            
        Returns:
            Generator yielding response steps
        """
        return self.agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]},
            stream_mode="values",
            config=self.config
        )

def run_cli():
    """Run the agent in CLI mode"""
    agent = MovieSearchAgent()
    
    print("Movie Search Agent - Interactive Chat")
    print("Type 'exit' or 'quit' to end the conversation")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break
                
            if not user_input:
                continue
                
            print("\nAgent: ", end='', flush=True)
            for step in agent.get_response(user_input):
                step["messages"][-1].pretty_print()
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    run_cli()