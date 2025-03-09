import streamlit as st
from agent import MovieSearchAgent
import os
from langchain_core.runnables import RunnableConfig
from utility import get_streamlit_cb, generate_thread_id
from dotenv import load_dotenv
from os import getenv
from config import (
    PAGE_TITLE, 
    PAGE_ICON, 
    API_KEY_MASK, 
    DEFAULT_SEARCH_ENGINE,
    AVAILABLE_SEARCH_ENGINES
)

load_dotenv()

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
st.title(f"{PAGE_ICON} {PAGE_TITLE}")

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_thread_id()
if "search_engine" not in st.session_state:
    st.session_state.search_engine = DEFAULT_SEARCH_ENGINE

# OpenAI API Key handling
openai_api_key = os.getenv("OPENAI_API_KEY")
with st.sidebar:
    if openai_api_key:
        st.text_input("OpenAI API Key (already set in environment)", value=API_KEY_MASK, disabled=True)
    else:
        user_api_key = st.text_input("OpenAI API Key", type="password")
        if user_api_key:
            openai_api_key = user_api_key
            os.environ["OPENAI_API_KEY"] = openai_api_key

# Sidebar configuration
with st.sidebar:
    # Search engine selector
    st.divider()
    
    # Determine available search engines based on credentials
    available_engines = ["duckduckgo"]  # DuckDuckGo is always available
    
    # Check if Google is available
    if all(getenv(env_var) for env_var in AVAILABLE_SEARCH_ENGINES["google"]):
        available_engines.append("google")
    
    # Set default index based on available engines
    default_index = 0
    if st.session_state.search_engine not in available_engines:
        st.session_state.search_engine = available_engines[0]
    else:
        default_index = available_engines.index(st.session_state.search_engine)
    
    selected_engine = st.selectbox(
        "Select Search Engine",
        available_engines,
        index=default_index,
        help="Choose which search engine to use for movie searches"
    )
    
    # Reset chat button
    if st.button("Reset Chat") or selected_engine != st.session_state.search_engine or not st.session_state.agent:
        st.session_state.search_engine = selected_engine
        if openai_api_key:
            try:
                st.session_state.agent = MovieSearchAgent(search_engine=selected_engine)
                st.session_state.messages = []
                st.session_state.thread_id = generate_thread_id()
                st.session_state.messages.append({"role": "assistant", "content": "How can I help you find movies today?"})
            except Exception as e:
                st.error(f"Failed to initialize agent: {str(e)}\n\nPlease check your API keys and try again. If the problem persists, ensure your environment is properly configured.")
        else:
            st.error("Please add your OpenAI API key to continue.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input(placeholder="Tell me about a movie..."):
    if not openai_api_key:
        st.error("Please add your OpenAI API key to continue.")
        st.stop()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            st_cb = get_streamlit_cb(st.container())
            cfg = RunnableConfig(max_concurrency=1)
            cfg["callbacks"] = [st_cb]
            cfg["configurable"] = {"thread_id": st.session_state.thread_id}
            
            # Show a loader
            with st.spinner("Let me cook..."):
                response = st.session_state.agent.get_complete_response(prompt, cfg)
                agent_response = response["messages"][-1].content
            
            # Replace the placeholder with the actual response
            message_placeholder.empty()
            st.write(agent_response)
            st.session_state.messages.append({"role": "assistant", "content": agent_response})
            
        except Exception as e:
            error_message = str(e)
            message_placeholder.empty()
            
            # Provide user-friendly error messages with debugging details
            if "API key" in error_message.lower():
                st.error(f"⚠️ API Key Issue: There was a problem with your OpenAI API key. Please check that it's valid and has sufficient credits.\n\nTechnical details: {error_message}")
            elif "rate limit" in error_message.lower():
                st.error(f"⚠️ Rate Limit Reached: You've reached the rate limit for API requests. Please try again in a few moments.\n\nTechnical details: {error_message}")
            elif "timeout" in error_message.lower():
                st.error(f"⚠️ Request Timeout: The request timed out. This might be due to high server load or a complex query. Please try again or simplify your question.\n\nTechnical details: {error_message}")
            else:
                st.error(f"⚠️ Unexpected Error: Something went wrong while processing your request. Please try again or try a different query.\n\nTechnical details: {error_message}")
            
            message_placeholder.error("Sorry, I encountered an error. Please check the error message above and try again.")