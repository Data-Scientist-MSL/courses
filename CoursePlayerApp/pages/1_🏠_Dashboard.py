"""
CoursePlayerApp - Dashboard

Main dashboard showing learning overview and quick actions.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Dashboard - GAI-Observe Academy",
    page_icon="🏠",
    layout="wide"
)

# Authentication check
if not st.session_state.get("authenticated"):
    st.warning("⚠️ Please log in to access this page")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# Get user info
user_id = st.session_state.get("user_id", "Unknown")
email = st.session_state.get("email", "user@example.com")
tier = st.session_state.get("tier", "basic")

# Header
col1, col2 = st.columns([3, 1])

with col1:
    st.title(f"Welcome back, {email.split('@')[0]}! 👋")

with col2:
    tier_colors = {"basic": "gray", "intermediate": "blue", "advanced": "gold"}
    st.markdown(f"**Tier:** :{tier_colors[tier]}[{tier.title()}]")

st.markdown("---")

# Key metrics
st.subheader("📊 Your Learning Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Courses In Progress", "2", delta="+1 this month")

with col2:
    st.metric("Avg Completion", "67%", delta="+12%")

with col3:
    st.metric("Certificates Earned", "1", delta="+1")

with col4:
    st.metric("Learning Streak", "7 days", delta="🔥")

st.markdown("---")

# Continue learning
st.subheader("📚 Continue Learning")

with st.container():
    st.markdown("**NLP with Transformers** - 67% Complete")
    st.progress(0.67)
    st.caption("Module 3: Attention Mechanisms")
    
    if st.button("Continue →", type="primary"):
        st.switch_page("pages/3_🎓_Course_Player.py")

st.markdown("---")

# Recommended next steps
st.subheader("🎯 Recommended Next Steps")

st.markdown("""
- ✅ Complete Module 3 Quiz (unlock Module 4)
- 🧪 Start Lab 3: Build Attention Layer
- 📄 Review slides for key concepts
- 🤖 Ask AI Tutor if you have questions
""")

st.markdown("---")

# Learning streak
st.subheader(f"🔥 Learning Streak: 7 days")
st.progress(7 / 30)
st.caption("Learn for 30 consecutive days to unlock the 'Month Master' badge!")

st.markdown("---")

# Quick actions
st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📚 Browse Courses", use_container_width=True):
        st.switch_page("pages/2_📚_My_Courses.py")

with col2:
    if st.button("📊 View Progress", use_container_width=True):
        st.switch_page("pages/5_📊_My_Progress.py")

with col3:
    if st.button("🎖️ My Certificates", use_container_width=True):
        st.switch_page("pages/6_🎖️_Certificates.py")

st.markdown("---")
st.caption("**Note**: This is a placeholder implementation. See documentation for full implementation details.")
