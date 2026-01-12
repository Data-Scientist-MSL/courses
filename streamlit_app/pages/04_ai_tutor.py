"""
AI Tutor - Chat with OLLAMA for learning assistance
"""

import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="AI Tutor", page_icon="🤖", layout="wide")

st.title("🤖 AI Tutor - Your Learning Assistant")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model selection
    available_models = ["llama3", "codellama", "mistral", "phi3"]
    selected_model = st.selectbox(
        "Select AI Model",
        available_models,
        help="Choose the model based on your needs"
    )
    
    # Model info
    model_info = {
        "llama3": "🧠 General purpose - Best for explanations and tutoring",
        "codellama": "💻 Code expert - Best for programming help",
        "mistral": "⚡ Fast - Best for quick questions",
        "phi3": "🪶 Lightweight - Best for low-resource devices"
    }
    
    st.info(model_info.get(selected_model, ""))
    
    # Temperature setting
    temperature = st.slider(
        "Temperature (creativity)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more focused"
    )
    
    st.markdown("---")
    
    # Clear chat
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "ollama_host" not in st.session_state:
    st.session_state.ollama_host = "http://localhost:11434"

# OLLAMA API function
def call_ollama(prompt, model, temperature=0.7):
    """Call OLLAMA API"""
    url = f"{st.session_state.ollama_host}/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        return f"❌ **Error**: Cannot connect to OLLAMA at {st.session_state.ollama_host}"
    except Exception as e:
        return f"❌ **Error**: {str(e)}"

# Main content
st.markdown("""
### How to Use the AI Tutor

**Ask about:** Data science, ML, programming, concepts, debugging

**Example questions:**
- "Explain transformers in simple terms"
- "Help me debug this code: [paste code]"
- "Create quiz questions about CNNs"
""")

st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner(f"🤔 Thinking..."):
            response = call_ollama(prompt, selected_model, temperature)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
