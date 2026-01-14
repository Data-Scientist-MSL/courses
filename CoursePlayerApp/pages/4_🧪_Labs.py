"""
CoursePlayerApp - Labs Page

This page displays the lab management interface with:
- Course selector
- Lab cards with status
- Launch buttons for interactive labs
- Completion tracking
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Labs - CoursePlayerApp",
    page_icon="🧪",
    layout="wide"
)

# Page content
st.title("🧪 Interactive Labs")

st.info("""
**📋 This is a placeholder page**

This page will display:
- Course selector dropdown
- Lab cards organized by module
- Lab status (not started, in progress, completed)
- Launch buttons to open SimulationPlayer
- Scores for completed labs

See `docs/courseplayerapp/UI_UX_DESIGN.md` for full specifications.
""")

# Course selector
st.selectbox("Select Course", ["Introduction to AI", "Machine Learning Basics", "NLP with Transformers"])

st.markdown("---")

# Lab cards
st.subheader("Module 1: AI Fundamentals")

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("**Lab 1: Python Basics for AI**")
        st.caption("Difficulty: Easy")
        st.success("✅ Completed • Score: 95/100")
        st.button("🔄 Retry", key="retry1", use_container_width=True)

with col2:
    with st.container():
        st.markdown("**Lab 2: Data Structures**")
        st.caption("Difficulty: Medium")
        st.info("⏳ In Progress")
        st.button("▶️ Continue", key="continue1", type="primary", use_container_width=True)

st.markdown("---")

st.subheader("Module 2: Machine Learning")

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("**Lab 3: Linear Regression**")
        st.caption("Difficulty: Medium")
        st.caption("Not started")
        
        # Basic tier restriction
        tier = st.session_state.get('tier', 'basic')
        if tier == 'basic':
            st.warning("🔒 Interactive labs available in Intermediate tier")
            st.button("Upgrade", key="upgrade_lab3", use_container_width=True)
        else:
            st.button("🚀 Start", key="start3", type="primary", use_container_width=True)

with col2:
    with st.container():
        st.markdown("**Lab 4: Decision Trees**")
        st.caption("Difficulty: Medium")
        st.caption("Not started")
        
        if tier == 'basic':
            st.warning("🔒 Interactive labs available in Intermediate tier")
            st.button("Upgrade", key="upgrade_lab4", use_container_width=True)
        else:
            st.button("🚀 Start", key="start4", type="primary", use_container_width=True)
