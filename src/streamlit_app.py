import streamlit as st
from agent import MovieSearchAgent
import os
from langchain_core.runnables import RunnableConfig
from utility import get_streamlit_cb, generate_thread_id
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Movie Search Agent", page_icon="🎬")
st.title("🎬 Movie Search Agent")

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "error" not in st.session_state:
    st.session_state.error = None
if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_thread_id()

# OpenAI API Key handling
openai_api_key = os.getenv("OPENAI_API_KEY")
with st.sidebar:
    if openai_api_key:
        st.text_input("OpenAI API Key (already set in environment)", value="••••••••••••••••••••••••", disabled=True)
    else:
        user_api_key = st.text_input("OpenAI API Key", type="password")
        if user_api_key:
            openai_api_key = user_api_key

# Display error message if present
if st.session_state.error:
    st.error(st.session_state.error)
    if st.button("Clear Error"):
        st.session_state.error = None
        

# Initialize or reset the agent
if st.sidebar.button("Reset Chat") or not st.session_state.agent:
    if openai_api_key:
        try:
            st.session_state.agent = MovieSearchAgent()
            st.session_state.messages = []
            st.session_state.thread_id = generate_thread_id()
            st.session_state.messages.append({"role": "assistant", "content": "How can I help you find movies today?"})
            st.session_state.error = None
        except Exception as e:
            st.session_state.error = f"Failed to initialize agent: {str(e)}\n\nPlease check your API keys and try again."
    else:
        st.session_state.error = "Please provide your OpenAI API key to continue."

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input(placeholder="Tell me about a movie..."):
    if not openai_api_key:
        st.session_state.error = "Please add your OpenAI API key to continue."
        st.experimental_rerun()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            st_cb = get_streamlit_cb(st.container())
            cfg = RunnableConfig()
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
            st.session_state.error = None
            
        except Exception as e:
            error_message = str(e)
            st.session_state.error = f"An error occurred: {error_message}"
            
            # Provide more user-friendly error messages
            if "API key" in error_message.lower():
                st.session_state.error = "There was an issue with your API key. Please check that it's valid and has sufficient credits."
            elif "rate limit" in error_message.lower():
                st.session_state.error = "You've reached the rate limit for API requests. Please try again in a few moments."
            elif "timeout" in error_message.lower():
                st.session_state.error = "The request timed out. This might be due to high server load or a complex query. Please try again or simplify your question."
            
            message_placeholder.error("Sorry, I encountered an error. Please check the error message and try again.")