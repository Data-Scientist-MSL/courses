"""
CoursePlayerApp - My Courses

Browse and access available courses based on user tier.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="My Courses - GAI-Observe Academy",
    page_icon="📚",
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
st.title("📚 My Courses")
st.markdown("---")

# Filters
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:
    search = st.text_input("🔍 Search courses", placeholder="Search by title or topic...")

with col2:
    category = st.selectbox("Category", ["All", "AI", "Data Science", "Machine Learning"])

with col3:
    difficulty = st.selectbox("Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])

with col4:
    sort_by = st.selectbox("Sort by", ["Recently Accessed", "Progress", "Alphabetical"])

st.markdown("---")

# Mock course data
mock_courses = [
    {"id": "ai-01", "title": "Introduction to AI", "progress": 100, "accessible": True},
    {"id": "ai-02", "title": "ML Fundamentals", "progress": 85, "accessible": True},
    {"id": "ai-03", "title": "NLP with Transformers", "progress": 67, "accessible": tier in ["intermediate", "advanced"]},
    {"id": "ai-04", "title": "Advanced Deep Learning", "progress": 0, "accessible": tier == "advanced"},
]

# Render accessible courses
accessible = [c for c in mock_courses if c["accessible"]]
locked = [c for c in mock_courses if not c["accessible"]]

st.subheader(f"Your Courses ({len(accessible)} accessible)")

cols = st.columns(3)

for i, course in enumerate(accessible):
    with cols[i % 3]:
        st.markdown(f"### {course['title']}")
        st.progress(course["progress"] / 100)
        st.caption(f"{course['progress']}% complete")
        
        if st.button(f"Continue Learning →", key=f"course_{course['id']}", use_container_width=True):
            st.session_state['current_course'] = course['id']
            st.switch_page("pages/3_🎓_Course_Player.py")

# Render locked courses
if locked:
    st.markdown("---")
    st.subheader(f"🔒 Unlock More Courses ({len(locked)})")
    
    cols = st.columns(3)
    
    for i, course in enumerate(locked):
        with cols[i % 3]:
            st.markdown(f"### {course['title']} 🔒")
            st.caption(f"Requires {'Advanced' if course['id'] == 'ai-04' else 'Intermediate'} tier")
            
            if st.button("Upgrade to Unlock", key=f"locked_{course['id']}", use_container_width=True):
                st.info("💡 Upgrade your tier to access this course!")

st.markdown("---")
st.caption("**Note**: This is a placeholder implementation. See documentation for full implementation details.")
