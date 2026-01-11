#!/usr/bin/env python3
"""
Interactive chatbot interface with OLLAMA using Streamlit.

Run with: streamlit run chatbot_interface.py
"""

import streamlit as st
import requests
import json


def ollama_chat(messages: list, model: str = "llama3") -> str:
    """Chat with OLLAMA API."""
    url = "http://localhost:11434/api/chat"
    
    data = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    return response.json()["message"]["content"]


def main():
    st.set_page_config(page_title="AI Tutor", page_icon="🤖", layout="wide")
    
    st.title("🤖 AI Data Science Tutor")
    st.markdown("Ask me anything about data science, machine learning, or programming!")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Model", ["llama3", "mistral", "phi3", "codellama"])
        
        role = st.selectbox("Tutor Role", [
            "General Data Science Tutor",
            "Python Expert",
            "Statistics Teacher",
            "Machine Learning Coach",
            "Code Reviewer"
        ])
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        # Add system prompt based on role
        system_prompts = {
            "General Data Science Tutor": "You are a helpful data science tutor. Explain concepts clearly with examples.",
            "Python Expert": "You are a Python programming expert. Provide clean, efficient code examples.",
            "Statistics Teacher": "You are a statistics teacher. Explain concepts with mathematical rigor and intuition.",
            "Machine Learning Coach": "You are an ML coach. Help with algorithms, implementation, and best practices.",
            "Code Reviewer": "You are a code reviewer. Provide constructive feedback on code quality and improvements."
        }
        
        st.session_state.messages.append({
            "role": "system",
            "content": system_prompts[role]
        })
    
    # Display chat history
    for msg in st.session_state.messages[1:]:  # Skip system message
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ollama_chat(st.session_state.messages, model=model)
                st.markdown(response)
        
        # Add to history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
