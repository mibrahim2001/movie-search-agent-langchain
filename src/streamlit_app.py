import streamlit as st
from agent import MovieSearchAgent
import os
from langchain_core.runnables import RunnableConfig
from utility import get_streamlit_cb
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Movie Search Agent", page_icon="🎬")
st.title("🎬 Movie Search Agent")

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []


# OpenAI API Key handling
openai_api_key = os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") else st.sidebar.text_input("OpenAI API Key", type="password")

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

# Initialize or reset the agent
if st.sidebar.button("Reset Chat") or not st.session_state.agent:
    if openai_api_key:
        st.session_state.agent = MovieSearchAgent()
        st.session_state.messages = []
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
        response = st.session_state.agent.get_complete_response(prompt, cfg)
        print(response)
        agent_response = response["messages"][-1].content
        st.write(agent_response)
        st.session_state.messages.append({"role": "assistant", "content": agent_response})
       
        