"""
CoursePlayerApp - Course Player Page

This is the main learning interface with:
- Module navigation in sidebar
- Video player with adaptive quality
- Slides viewer
- Lab launcher
- AI Tutor (tier-dependent)
- Progress tracking
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Course Player - CoursePlayerApp",
    page_icon="🎓",
    layout="wide"
)

# Sidebar: Module navigation
with st.sidebar:
    st.title("Course Navigation")
    st.caption("Introduction to AI")
    
    st.markdown("---")
    st.subheader("📑 Modules")
    
    with st.expander("Module 1: AI Fundamentals (100%)", expanded=True):
        st.button("✅ What is AI?", key="v1")
        st.button("✅ History of AI", key="v2")
        st.button("📝 Module 1 Quiz", key="q1")
    
    with st.expander("Module 2: Machine Learning (60%)"):
        st.button("✅ Introduction to ML", key="v3")
        st.button("▶️ Supervised Learning", key="v4")
        st.button("⭕ Unsupervised Learning", key="v5")
        st.button("📝 Module 2 Quiz", key="q2")
    
    st.markdown("---")
    st.subheader("🤖 AI Tutor")
    st.info("AI Tutor available in Intermediate tier")
    st.button("Upgrade to unlock", use_container_width=True)

# Main content
st.title("🎓 Course Player")

st.info("""
**📋 This is a placeholder page**

This page will display:
- Module navigation in left sidebar
- Video player with adaptive quality based on tier
- Tabbed interface (Video, Slides, Info)
- Progress bar at bottom
- AI Tutor chat in sidebar (if enabled)

See `docs/courseplayerapp/UI_UX_DESIGN.md` for full specifications.
""")

# Tabs
tab1, tab2, tab3 = st.tabs(["📹 Video", "📊 Slides", "ℹ️ Info"])

with tab1:
    st.subheader("What is Artificial Intelligence?")
    st.video("https://www.youtube.com/watch?v=ad79nYk2keg")
    
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("**Playback Controls**")
        st.selectbox("Speed", [0.5, 0.75, 1.0, 1.25, 1.5, 2.0], index=2)
    
    with col2:
        st.info("🔒 Download available in Intermediate tier")

with tab2:
    st.subheader("Lecture Slides")
    st.info("Slides viewer will be displayed here")
    st.image("https://via.placeholder.com/800x600", use_column_width=True)

with tab3:
    st.subheader("Course Information")
    st.write("""
    **Description:**
    This course introduces the fundamentals of Artificial Intelligence, covering key concepts, 
    history, and applications in modern technology.
    
    **Prerequisites:**
    - Basic programming knowledge
    - High school mathematics
    
    **What you'll learn:**
    - Definition and scope of AI
    - History and evolution of AI
    - Key AI techniques and algorithms
    - Real-world applications
    """)

# Progress bar
st.markdown("---")
col1, col2 = st.columns([4, 1])

with col1:
    st.progress(0.67)
    st.caption("Course Progress: 67%")

with col2:
    st.button("📊 View Detailed Progress")
