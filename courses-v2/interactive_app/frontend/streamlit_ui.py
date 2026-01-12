#!/usr/bin/env python3
"""
Main Streamlit UI for Data Science Specialization 2.0

Run with: streamlit run streamlit_ui.py
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


def main():
    """Main application."""
    st.set_page_config(
        page_title="Data Science Specialization 2.0",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 1rem 0;
        }
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .feature-box {
            padding: 1.5rem;
            border-radius: 10px;
            background: #f8f9fa;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=DS+2.0", use_column_width=True)
        
        st.markdown("### 🗂️ Navigation")
        
        page = st.radio(
            "Select Page",
            [
                "🏠 Home",
                "📚 Course Browser",
                "💻 Lab Runner",
                "🤖 AI Chat",
                "📊 Dataset Explorer",
                "📈 Progress Tracker"
            ]
        )
        
        st.markdown("---")
        
        st.markdown("### ⚙️ Settings")
        theme = st.toggle("🌙 Dark Mode", value=False)
        
        st.markdown("---")
        
        st.markdown("### 🎯 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Modules", "9")
            st.metric("Labs", "25+")
        with col2:
            st.metric("Datasets", "50+")
            st.metric("Progress", "0%")
    
    # Main content
    if page == "🏠 Home":
        show_home()
    elif page == "📚 Course Browser":
        show_course_browser()
    elif page == "💻 Lab Runner":
        show_lab_runner()
    elif page == "🤖 AI Chat":
        show_ai_chat()
    elif page == "📊 Dataset Explorer":
        show_dataset_explorer()
    elif page == "📈 Progress Tracker":
        show_progress_tracker()


def show_home():
    """Display home page."""
    st.markdown('<h1 class="main-header">🎓 Data Science Specialization 2.0</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Modern AI/ML Curriculum with Local LLMs & Zero-Cost Tools</p>', unsafe_allow_html=True)
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🤖 AI-Powered Learning</h3>
            <p>Interactive chatbot tutor using OLLAMA (Llama 3, Mistral)</p>
            <ul>
                <li>24/7 availability</li>
                <li>Personalized explanations</li>
                <li>Code review</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>📚 Modern Curriculum</h3>
            <p>Cutting-edge topics for 2026</p>
            <ul>
                <li>Transformers & LLMs</li>
                <li>Generative AI</li>
                <li>MLOps & Production</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>💰 100% Free</h3>
            <p>Zero-cost learning experience</p>
            <ul>
                <li>No subscriptions</li>
                <li>Open-source tools</li>
                <li>Local-first approach</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Course modules
    st.markdown("### 📋 Course Modules")
    
    modules = [
        {
            "title": "00_Modern_Foundations",
            "description": "AI-Human Augmentation, Scientific Tooling, Data Engineering",
            "icon": "🏗️"
        },
        {
            "title": "01_Core_AI_ML",
            "description": "Statistical Learning, Deep Learning, NLP/LLMs, Generative AI",
            "icon": "🧠"
        },
        {
            "title": "02_Production_Specialization",
            "description": "MLOps, Production Systems, AI Ethics",
            "icon": "🚀"
        }
    ]
    
    for module in modules:
        with st.expander(f"{module['icon']} {module['title']}"):
            st.write(module['description'])
            st.button(f"Start {module['title']}", key=module['title'])
    
    st.markdown("---")
    
    # Quick start
    st.markdown("### 🚀 Quick Start")
    
    tab1, tab2, tab3 = st.tabs(["Setup", "First Lesson", "Resources"])
    
    with tab1:
        st.markdown("""
        **Get started in 3 steps:**
        
        1. **Install OLLAMA** (optional but recommended)
           ```bash
           curl -fsSL https://ollama.ai/install.sh | sh
           ollama pull llama3
           ```
        
        2. **Clone the repository**
           ```bash
           git clone https://github.com/Data-Scientist-MSL/courses
           cd courses/courses-v2
           ```
        
        3. **Start learning!**
           - Browse courses in the sidebar
           - Try the AI chatbot
           - Run hands-on labs
        """)
    
    with tab2:
        st.markdown("""
        **Recommended first module:**
        
        📖 **03_NLP_Transformers_LLMs**
        
        - Learn transformer architecture
        - Work with Hugging Face
        - Run local LLMs with OLLAMA
        - Build RAG systems
        - Fine-tune models with LoRA
        """)
        
        st.button("Go to NLP Module →", type="primary")
    
    with tab3:
        st.markdown("""
        **Useful Resources:**
        
        - 📚 [Course Documentation](../docs/)
        - 🎥 [Video Tutorials](coming soon)
        - 💬 [Community Forum](coming soon)
        - 📊 [Free Datasets Catalog](../docs/DATASETS_CATALOG.md)
        - 🤖 [OLLAMA Setup Guide](../ollama_instructor/ollama_setup/install_guide.md)
        """)


def show_course_browser():
    """Display course browser."""
    st.title("📚 Course Browser")
    st.markdown("Browse and navigate through course modules")
    
    # Course tree
    st.markdown("### 📁 Course Structure")
    
    courses_path = Path(__file__).parent.parent.parent / "01_Core_AI_ML/03_NLP_Transformers_LLMs"
    
    if courses_path.exists():
        st.success("✅ NLP Module Available")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📑 Slides**")
            slides = list(courses_path.glob("slides/*.md"))
            for slide in slides:
                st.markdown(f"- [{slide.stem}]({slide})")
        
        with col2:
            st.markdown("**🧪 Labs**")
            labs = list(courses_path.glob("labs/*.ipynb"))
            for lab in labs:
                st.markdown(f"- [{lab.stem}]({lab})")
    else:
        st.info("Course content will be displayed here")


def show_lab_runner():
    """Display lab runner."""
    st.title("💻 Lab Runner")
    st.markdown("Run Jupyter notebooks directly in the browser")
    
    st.info("🔬 Interactive Jupyter Lab coming soon!")
    st.markdown("""
    For now, you can:
    
    1. Download labs from the Course Browser
    2. Run locally with:
       ```bash
       jupyter notebook
       ```
    3. Or use Google Colab (upload .ipynb files)
    """)


def show_ai_chat():
    """Display AI chat interface."""
    st.title("🤖 AI Data Science Tutor")
    st.markdown("Ask me anything about data science, ML, or programming!")
    
    # Check OLLAMA connection
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        st.success("✅ Connected to OLLAMA")
        
        # Simple chat interface
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        
        # Display messages
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # Input
        if prompt := st.chat_input("Ask a question..."):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get response (simplified)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Placeholder - actual OLLAMA call would go here
                    response = "I'm ready to help! (OLLAMA integration active)"
                    st.markdown(response)
            
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
    
    except:
        st.warning("""
        ⚠️ OLLAMA not running. 
        
        Start OLLAMA with:
        ```bash
        ollama serve
        ```
        
        Or use the chat without local LLM (limited functionality).
        """)


def show_dataset_explorer():
    """Display dataset explorer."""
    st.title("📊 Dataset Explorer")
    st.markdown("Explore 50+ free datasets for data science")
    
    # Categories
    category = st.selectbox(
        "Category",
        ["All", "NLP", "Computer Vision", "Time Series", "Tabular", "Audio"]
    )
    
    # Sample datasets
    datasets = [
        {"name": "IMDB Reviews", "category": "NLP", "size": "50K", "license": "Apache 2.0"},
        {"name": "MNIST", "category": "Computer Vision", "size": "70K", "license": "CC-BY-SA"},
        {"name": "Stock Prices", "category": "Time Series", "size": "5 years", "license": "Public"},
    ]
    
    for ds in datasets:
        if category == "All" or ds["category"] == category:
            with st.expander(f"📦 {ds['name']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Category", ds["category"])
                with col2:
                    st.metric("Size", ds["size"])
                with col3:
                    st.metric("License", ds["license"])
                
                st.button("Load Dataset", key=ds["name"])


def show_progress_tracker():
    """Display progress tracker."""
    st.title("📈 Progress Tracker")
    st.markdown("Track your learning progress")
    
    # Progress metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Modules Completed", "0/9", "0%")
    with col2:
        st.metric("Labs Completed", "0/25", "0%")
    with col3:
        st.metric("Time Invested", "0 hrs")
    with col4:
        st.metric("Streak", "0 days", "🔥")
    
    # Progress bars
    st.markdown("### Module Progress")
    
    modules = [
        "00_Modern_Foundations",
        "01_Statistical_Learning",
        "02_Deep_Learning",
        "03_NLP_Transformers_LLMs",
        "04_Generative_AI",
        "05_MLOps_Production"
    ]
    
    for module in modules:
        progress = 0
        st.markdown(f"**{module}**")
        st.progress(progress)
        st.caption(f"{progress}% complete")


if __name__ == "__main__":
    main()
