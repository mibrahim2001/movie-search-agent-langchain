from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from tools.search_tool_kit import SearchToolKit
from utility import load_system_prompt
from langgraph.checkpoint.memory import MemorySaver
from typing import Generator, Dict, Any
from langchain_core.runnables import RunnableConfig
from typing import Optional
from langchain_openai import ChatOpenAI
from os import getenv
class MovieSearchAgent:
    def __init__(self, model_name: str = "gpt-4o-mini", model_provider: str = "openai"):
        load_dotenv()
        
        # Initialize components
        self.memory = MemorySaver()
        self.search_toolkit = SearchToolKit()
        self.tools = self.search_toolkit.get_tools()
        
        # Initialize model and agent
        self.model = ChatOpenAI(
            openai_api_key=getenv("OPENROUTER_API_KEY"),
            openai_api_base=getenv("OPENROUTER_BASE_URL"),
            model_name=model_name,
        )
        self.system_message = load_system_prompt()
        self.agent_executor = create_react_agent(
            self.model,
            self.tools,
            prompt=self.system_message,
            checkpointer=self.memory
        )

    def invoke_agent(self, user_input: str, config: RunnableConfig) -> Generator[Dict[str, Any], None, None]:
        """
        Invoke the agent to process the given user input and return a response stream.
        
        Args:
            user_input (str): The user's input message to be processed by the agent.
            config (RunnableConfig): Configuration settings for invoking the agent.
            
        Returns:
            Generator[Dict[str, Any], None, None]: A generator yielding response steps from the agent.
        """
        return self.agent_executor.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )

    def generate_response_stream(self, user_input: str, config: Optional[RunnableConfig] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Get streaming response from the agent for a given user input.
        
        Args:
            user_input (str): The user's input message
            config (Optional[RunnableConfig]): Optional configuration for the response stream
        Returns:
            Generator yielding response steps
        """
        return self.agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]},
            stream_mode="values",
            config=config
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