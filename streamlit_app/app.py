"""
Data Science 2.0 - Main Streamlit Application
Interactive learning platform with AI tutor integration
"""

import streamlit as st
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Data Science 2.0",
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
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x100/1f77b4/ffffff?text=DS+2.0", use_container_width=True)
    st.title("🎓 Navigation")
    
    st.markdown("---")
    
    # Course selection
    st.subheader("📚 Learning Tracks")
    track = st.selectbox(
        "Select Track",
        [
            "🏠 Home",
            "🌟 Track 0: Modern Foundations",
            "🤖 Track 1: Core AI/ML",
            "🚀 Track 2: Production & Ethics",
            "🧠 AI Instructor System"
        ]
    )
    
    st.markdown("---")
    
    # Quick links
    st.subheader("🔗 Quick Links")
    st.markdown("""
    - [📖 Curriculum](docs/CURRICULUM_DESIGN.md)
    - [🚀 Setup Guide](docs/SETUP_GUIDE.md)
    - [📊 Datasets](docs/DATASETS_CATALOG.md)
    - [🤖 AI Tutor Guide](docs/AI_INSTRUCTOR_GUIDE.md)
    - [🧠 Philosophy](docs/AUGMENTED_HUMAN_PHILOSOPHY.md)
    """)
    
    st.markdown("---")
    
    # Progress tracker
    st.subheader("📈 Your Progress")
    st.progress(0.35, text="35% Complete")
    st.caption("🎯 Keep going! You're doing great!")

# Main content
if track == "🏠 Home":
    # Hero section
    st.markdown('<h1 class="main-header">🎓 Data Science Specialization 2.0</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;">
        <strong>Modernized Curriculum</strong> • <strong>AI-Powered Learning</strong> • <strong>100% Free</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Key features
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>50+</h2>
            <p>Free Datasets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>0$</h2>
            <p>Zero Cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>24/7</h2>
            <p>AI Tutor</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2>2026</h2>
            <p>Latest Tech</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main features
    st.markdown('<h2 class="sub-header">✨ What Makes This Special?</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI-Powered", "📊 Modern Stack", "🧠 Philosophy", "🎯 Practical"])
    
    with tab1:
        st.markdown("""
        ### 🤖 OLLAMA AI Instructor
        
        Your personal AI tutor powered by local LLMs:
        - **24/7 Availability**: Ask questions anytime
        - **Privacy-First**: All processing happens on your machine
        - **Multi-Model Support**: Llama 3, CodeLlama, Mistral
        - **Adaptive Learning**: Personalized to your pace
        
        **Try it now**: Go to AI Tutor page and ask anything!
        """)
        
        st.code("""
# Example: Ask the AI tutor
"Explain transformers in simple terms"
"Help me debug this PyTorch code"
"Generate quiz questions on CNNs"
        """, language="python")
    
    with tab2:
        st.markdown("""
        ### 📊 2026 Technology Stack
        
        Learn the tools that matter today:
        
        **Deep Learning**:
        - PyTorch & TensorFlow
        - Transformers (BERT, GPT)
        - Hugging Face ecosystem
        
        **LLMs & GenAI**:
        - OLLAMA for local inference
        - LangChain for RAG
        - Vector databases (Chroma)
        
        **MLOps**:
        - Docker containerization
        - FastAPI model serving
        - MLflow experiment tracking
        """)
    
    with tab3:
        st.markdown("""
        ### 🧠 Augmented Human Philosophy
        
        **Core Principle**: AI augments humans, doesn't replace them
        
        **You'll Learn**:
        - AI as cognitive extension ("second brain")
        - Scientific tooling for everyday life
        - Ethical AI collaboration
        - Data-driven decision making
        
        **Practical Applications**:
        - Personal knowledge assistant with RAG
        - Quantified self dashboard
        - Productivity analyzer
        - Email/meeting auto-summarizer
        """)
        
        st.info("💡 See full philosophy guide in documentation")
    
    with tab4:
        st.markdown("""
        ### 🎯 Hands-On & Practical
        
        **50+ Labs** across all modules:
        - Real datasets from healthcare, finance, NLP, vision
        - Step-by-step Jupyter notebooks
        - Code you can use immediately
        - Projects for your portfolio
        
        **Example Projects**:
        1. Build a chatbot with OLLAMA
        2. Create RAG system for personal notes
        3. Fine-tune transformer for sentiment analysis
        4. Deploy ML model with Docker + FastAPI
        5. Build productivity analytics dashboard
        """)
    
    st.markdown("---")
    
    # Getting started
    st.markdown('<h2 class="sub-header">🚀 Get Started in 5 Minutes</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Quick Start with Docker
        
        ```bash
        # Clone repository
        git clone https://github.com/Data-Scientist-MSL/courses.git
        cd courses
        
        # Start all services
        docker-compose up -d
        
        # Download AI models
        docker-compose exec ollama ollama pull llama3
        
        # Open app
        # http://localhost:8501
        ```
        """)
    
    with col2:
        st.markdown("""
        ### Local Python Setup
        
        ```bash
        # Create virtual environment
        python -m venv venv
        source venv/bin/activate  # or venv\\Scripts\\activate on Windows
        
        # Install dependencies
        pip install -r requirements.txt
        
        # Install OLLAMA
        curl -fsSL https://ollama.ai/install.sh | sh
        ollama pull llama3
        
        # Run app
        streamlit run streamlit_app/app.py
        ```
        """)
    
    st.success("✅ See full setup guide in documentation")
    
    st.markdown("---")
    
    # Learning path
    st.markdown('<h2 class="sub-header">📚 Learning Path</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Recommended Learning Sequence
    
    1. **Track 0: Modern Foundations** (3 weeks)
       - Philosophy of AI-Human Augmentation
       - Scientific Tooling Ecosystem
       - Modern Data Engineering
    
    2. **Track 1: Core AI/ML** (8 weeks)
       - Statistical Learning Enhanced
       - Deep Learning Foundations
       - ⭐ **NLP, Transformers & LLMs** (Sample Module Complete!)
       - Generative AI Applications
    
    3. **Track 2: Production & Ethics** (4 weeks)
       - MLOps & Production Deployment
       - AI Ethics & Responsible AI
    
    **Total Duration**: 6-9 months (10-15 hours/week, self-paced)
    """)
    
    # CTA
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 Browse Courses", use_container_width=True):
            st.switch_page("pages/01_course_browser.py")
    
    with col2:
        if st.button("🔬 Try Sample Lab", use_container_width=True):
            st.switch_page("pages/02_lab_runner.py")
    
    with col3:
        if st.button("🤖 Chat with AI Tutor", use_container_width=True):
            st.switch_page("pages/04_ai_tutor.py")

elif "Track 0" in track:
    st.title("🌟 Track 0: Modern Foundations")
    st.info("📝 Content coming soon! Sample module (NLP & Transformers) is complete in Track 1.")
    
    st.markdown("""
    ### Modules in This Track:
    
    1. **Philosophy of AI-Human Augmentation**
       - AI as cognitive extension
       - Ethical collaboration principles
       - See: `docs/AUGMENTED_HUMAN_PHILOSOPHY.md`
    
    2. **Scientific Tooling Ecosystem**
       - Python, Jupyter, VS Code
       - Git and version control
       - Docker basics
    
    3. **Modern Data Engineering**
       - Data pipelines
       - Vector databases
       - Real-time processing
    """)

elif "Track 1" in track:
    st.title("🤖 Track 1: Core AI/ML")
    
    st.markdown("""
    ### Available Modules:
    
    #### ⭐ Module 3: NLP, Transformers & LLMs (Complete!)
    This is our **complete sample module** demonstrating the full course structure:
    
    - **📊 Slides**: Marp-formatted lectures on transformer architecture
    - **🏗️ Diagrams**: 10 Mermaid diagrams explaining concepts
    - **🔬 Labs**: 4 Jupyter notebooks with hands-on exercises
    - **📚 Datasets**: Links to free NLP datasets
    - **💡 Practical Insights**: Real-world applications
    
    **What's Included**:
    - Lecture 1: Transformer Architecture
    - Lab 1: Hugging Face Transformers
    - Architecture diagrams (attention, encoder-decoder, etc.)
    - Practical guides for personal knowledge assistant
    """)
    
    with st.expander("📖 View Module Contents"):
        st.markdown("""
        **Slides** (`01_Core_AI_ML/03_NLP_Transformers_LLMs/slides/`):
        - `01_transformer_architecture.md` - Complete 30+ slide deck
        
        **Architecture** (`architecture/`):
        - `transformer_attention.mermaid` - 10 interactive diagrams
        
        **Labs** (`labs/`):
        - `lab01_huggingface_transformers.ipynb` - Complete hands-on notebook
        
        **Practical Insights** (`practical_insights/`):
        - Personal knowledge assistant guide
        - Email summarizer project
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### Other Modules (Coming Soon):
    1. Statistical Learning Enhanced
    2. Deep Learning Foundations
    4. Generative AI Applications
    """)

elif "Track 2" in track:
    st.title("🚀 Track 2: Production & Ethics")
    st.info("📝 Content coming soon!")

else:  # AI Instructor System
    st.title("🧠 AI Instructor System")
    
    st.markdown("""
    ### OLLAMA-Powered Learning Assistant
    
    The AI Instructor system provides:
    
    1. **Lecture Generation** 📝
       - Auto-generate slides from topics
       - Create architecture diagrams
       - See: `03_AI_Instructor_System/lecture_generator/`
    
    2. **Interactive Tutor** 💬
       - 24/7 Q&A assistance
       - Code explanation and debugging
       - Try it: Go to "AI Tutor" page
    
    3. **Quiz Generator** 🎯
       - Adaptive assessments
       - Instant feedback
       - See: `03_AI_Instructor_System/quiz_generator/`
    
    ### Available Models:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Llama 3 (8B)**
        - General tutoring
        - Concept explanation
        - Study assistance
        
        **Mistral (7B)**
        - Fast responses
        - Quick Q&A
        - Resource-efficient
        """)
    
    with col2:
        st.markdown("""
        **CodeLlama (13B)**
        - Code generation
        - Debugging help
        - Code review
        
        **Phi-3 (3.8B)**
        - Lightweight option
        - Low RAM devices
        - Basic tutoring
        """)
    
    st.markdown("---")
    st.info("📚 See full guide: `docs/AI_INSTRUCTOR_GUIDE.md`")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>Data Science Specialization 2.0</strong> • Version 2.0.0 • January 2026</p>
    <p>🎓 Built with ❤️ using Streamlit, OLLAMA, and 100% open-source tools</p>
    <p>📄 Licensed under CC-NC-SA • 🌟 Star us on <a href="https://github.com/Data-Scientist-MSL/courses">GitHub</a></p>
</div>
""", unsafe_allow_html=True)
