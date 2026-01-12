"""
CoursePlayerApp - Labs

List all labs with status and launch links.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Labs - GAI-Observe Academy",
    page_icon="🧪",
    layout="wide"
)

# Authentication check
if not st.session_state.get("authenticated"):
    st.warning("⚠️ Please log in to access this page")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

tier = st.session_state.get("tier", "basic")

# Header
st.title("🧪 Labs")
st.caption("Hands-on coding exercises to reinforce learning")
st.markdown("---")

# Course selector
course = st.selectbox("Select Course", ["NLP with Transformers", "Machine Learning Fundamentals"])

st.markdown("---")

# Mock lab data
labs = [
    {
        "id": "lab1",
        "title": "Tokenization Basics",
        "duration": "60 min",
        "status": "completed",
        "score": 95
    },
    {
        "id": "lab2",
        "title": "Build Attention Layer",
        "duration": "90 min",
        "status": "in_progress",
        "score": 0
    },
    {
        "id": "lab3",
        "title": "Fine-tune BERT",
        "duration": "120 min",
        "status": "locked",
        "score": 0
    },
]

for lab in labs:
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            if lab["status"] == "completed":
                st.markdown(f"### {lab['title']} ✅")
            elif lab["status"] == "in_progress":
                st.markdown(f"### {lab['title']} ⏳")
            else:
                st.markdown(f"### {lab['title']} 🔒")
            
            st.caption(f"Duration: {lab['duration']}")
        
        with col2:
            if lab["status"] == "completed":
                st.metric("Score", f"{lab['score']}%")
            elif lab["status"] == "in_progress":
                st.metric("Progress", "0%")
            else:
                st.caption("Requires: Complete Module 3 Quiz")
        
        with col3:
            if lab["status"] == "completed":
                if st.button("Review Results", key=f"review_{lab['id']}", use_container_width=True):
                    st.toast("Opening results...")
            
            elif lab["status"] == "in_progress":
                if tier in ["intermediate", "advanced"]:
                    if st.button("🚀 Start Lab", key=f"start_{lab['id']}", type="primary", use_container_width=True):
                        st.info("Lab would launch in SimulationPlayer (integration pending)")
                else:
                    if st.button("🔒 Start Lab", key=f"locked_{lab['id']}", disabled=True, use_container_width=True):
                        pass
                    st.caption("Interactive labs require Intermediate tier")
            
            else:
                if st.button("Locked", key=f"locked_{lab['id']}", disabled=True, use_container_width=True):
                    pass
        
        st.markdown("---")

# Basic tier message
if tier == "basic":
    st.info("""
    🔒 **Interactive labs are available in Intermediate tier ($247)**
    
    With Intermediate tier, you can:
    - Execute code in interactive environments
    - Get real-time feedback
    - Save your progress
    - Access hints and solutions
    
    Basic tier users can view lab descriptions and sample code in read-only mode.
    """)
    
    if st.button("⬆️ Upgrade to Intermediate"):
        st.toast("Redirecting to upgrade page...")

st.markdown("---")
st.caption("**Note**: This is a placeholder implementation. See documentation for full implementation details.")
