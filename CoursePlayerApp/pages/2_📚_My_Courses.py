"""
CoursePlayerApp - My Courses Page

This page displays the course catalog with:
- Search and filter functionality
- Grid/list view toggle
- Course cards with progress
- Locked courses with upgrade prompts
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="My Courses - CoursePlayerApp",
    page_icon="📚",
    layout="wide"
)

# Page content
st.title("📚 My Courses")

st.info("""
**📋 This is a placeholder page**

This page will display:
- Search bar to find courses
- Filters (category, difficulty, status)
- Grid/list view toggle
- Course cards showing title, thumbnail, progress, and duration
- Locked courses with upgrade prompts

See `docs/courseplayerapp/UI_UX_DESIGN.md` for full specifications.
""")

# Placeholder filters
col1, col2, col3, col4 = st.columns([2, 1, 1, 2])

with col1:
    st.text_input("🔍 Search courses", placeholder="e.g., Machine Learning")

with col2:
    st.selectbox("Category", ["All", "AI", "Data Science", "ML"])

with col3:
    st.selectbox("Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])

with col4:
    st.radio("View", ["Grid", "List"], horizontal=True)

st.markdown("---")

# Placeholder course cards
st.subheader("Available Courses")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://via.placeholder.com/300x200", use_column_width=True)
    st.markdown("**Introduction to AI**")
    st.caption("Beginner • 12h")
    st.progress(0.3)
    st.caption("30% complete")
    st.button("▶️ Continue", key="course1", use_container_width=True)

with col2:
    st.image("https://via.placeholder.com/300x200", use_column_width=True)
    st.markdown("**Machine Learning Basics**")
    st.caption("Beginner • 15h")
    st.progress(0.0)
    st.caption("Not started")
    st.button("▶️ Start", key="course2", use_container_width=True)

with col3:
    st.image("https://via.placeholder.com/300x200", use_column_width=True)
    st.markdown("**Deep Learning & Neural Networks**")
    st.caption("Advanced • 20h")
    st.warning("🔒 Advanced tier required")
    st.button("Upgrade", key="upgrade1", use_container_width=True)
