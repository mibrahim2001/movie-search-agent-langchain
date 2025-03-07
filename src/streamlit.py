import streamlit as st
from agent import MovieSearchAgent
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.callbacks import StreamlitCallbackHandler
import os

st.set_page_config(page_title="Movie Search Agent", page_icon="🎬")
st.title("Movie Search Agent")

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# OpenAI API Key handling
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
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
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the agent's response
        for step in st.session_state.agent.get_response(prompt):
            print(step)
            print("--------------------------------")
            response = step["messages"][-1].content
            full_response = response
            message_placeholder.write(full_response)
        
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})