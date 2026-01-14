"""
CoursePlayerApp - Dashboard Page

This page displays the user's learning dashboard with:
- Quick stats (courses in progress, completion rate, etc.)
- Continue learning section
- Recent activity feed
- Upgrade CTA for non-Advanced users
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Dashboard - CoursePlayerApp",
    page_icon="🏠",
    layout="wide"
)

# Page content
st.title("🏠 Dashboard")

st.info("""
**📋 This is a placeholder page**

This page will display:
- Welcome message with user's name
- Quick stats (courses in progress, completion rate, certificates, streak)
- Continue learning section (resume last course)
- Recent activity feed
- Upgrade CTA for non-Advanced users

See `docs/courseplayerapp/UI_UX_DESIGN.md` for full specifications.
""")

# Placeholder content
st.subheader("Welcome back, Student!")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Courses In Progress", "3", delta="+1")

with col2:
    st.metric("Completion Rate", "67%", delta="+12%")

with col3:
    st.metric("Certificates Earned", "2")

with col4:
    st.metric("Current Streak", "7 days", delta="🔥")

st.markdown("---")

st.subheader("📚 Continue Learning")
st.info("Select a course from My Courses to start learning")

st.markdown("---")

st.subheader("🕐 Recent Activity")
st.write("Your recent learning activities will appear here")
