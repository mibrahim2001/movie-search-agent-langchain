import streamlit as st
from agent import MovieSearchAgent
import os
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from utility import get_streamlit_cb
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="Movie Search Agent", page_icon="🎬")
st.title("Movie Search Agent")

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "steps" not in st.session_state:
    st.session_state.steps = {}

# OpenAI API Key handling
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

# Initialize or reset the agent
if st.sidebar.button("Reset Chat") or not st.session_state.agent:
    if openai_api_key:
        st.session_state.agent = MovieSearchAgent()
        st.session_state.messages = []
        st.session_state.steps = {}
        st.session_state.messages.append({"role": "assistant", "content": "How can I help you find movies today?"})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input(placeholder="Tell me about a movie..."):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        st_cb = get_streamlit_cb(st.container())
        cfg = RunnableConfig()
        cfg["callbacks"] = [st_cb]
        cfg["configurable"] = {"thread_id": "abc123"}
        response = st.session_state.agent.invoke_agent(prompt, cfg)
        print(response)

        agent_response = response["messages"][-1].content
        st.write(agent_response)

        st.session_state.steps[str(len(st.session_state.messages) - 1)] = response["messages"][1:len(response["messages"])-1]

        st.session_state.messages.append({"role": "assistant", "content": agent_response})
       
        # message_placeholder = st.empty()
        # full_response = ""
        
        # # Stream the agent's response
        # for step in st.session_state.agent.get_response(prompt):
        #     message = step["messages"][-1]
        #     print("Type: ", message.type)
        #     if message.type == "ai":
        #         if message.tool_calls:
        #             for tool_call in message.tool_calls:
        #                 print(f"Tool call: {tool_call['name']}")
        #                 print(f"Tool call input: {tool_call['args']}")
        #         else:
        #             print(f"Message: {message.content}")
        #             message_placeholder.write(message.content)
        #     elif message.type == "tool":
        #         print(message.content[:100])
        #     print("--------------------------------")
        #     full_response = message.content
        
        # # Add assistant's response to chat history
        # st.session_state.messages.append({"role": "assistant", "content": full_response})