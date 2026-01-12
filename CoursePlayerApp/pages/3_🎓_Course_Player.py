"""
CoursePlayerApp - Course Player

Video player, slides viewer, and AI Tutor interface.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Course Player - GAI-Observe Academy",
    page_icon="🎓",
    layout="wide"
)

# Authentication check
if not st.session_state.get("authenticated"):
    st.warning("⚠️ Please log in to access this page")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

tier = st.session_state.get("tier", "basic")
current_course = st.session_state.get("current_course", "ai-03")

# Header
st.title("NLP with Transformers")
st.caption("Learn modern natural language processing with transformer architectures")
st.markdown("---")

# Layout: Sidebar (navigation) + Main (player) + Sidebar (AI Tutor)
col1, col2, col3 = st.columns([1, 3, 1])

# Left: Module navigation
with col1:
    st.subheader("📑 Modules")
    
    modules = [
        {"id": "module-01", "title": "Introduction to NLP", "status": "✅"},
        {"id": "module-02", "title": "Transformers", "status": "⏳"},
        {"id": "module-03", "title": "Attention Mechanisms", "status": "▶️"},
        {"id": "module-04", "title": "Fine-tuning", "status": "🔒"},
    ]
    
    for module in modules:
        with st.expander(f"{module['status']} {module['title']}", expanded=module['status']=='▶️'):
            if st.button("📹 Video 1: Introduction", key=f"{module['id']}_v1"):
                st.toast("Video selected!")
            if st.button("📄 Slides", key=f"{module['id']}_slides"):
                st.toast("Slides selected!")
            if st.button("🧪 Lab", key=f"{module['id']}_lab"):
                st.switch_page("pages/4_🧪_Labs.py")

# Center: Content player
with col2:
    st.subheader("📹 Video: Understanding Attention Mechanisms")
    
    # Placeholder for video
    st.video("https://www.youtube.com/watch?v=aircAruvnKk")  # Demo video
    
    # Video controls
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.selectbox("Playback Speed", ["0.5x", "1x", "1.25x", "1.5x", "2x"], index=1)
    
    with col_b:
        st.selectbox("Captions", ["Off", "English"], index=1)
    
    with col_c:
        st.metric("Quality", "720p" if tier in ["intermediate", "advanced"] else "480p")
    
    # Download section
    st.markdown("---")
    st.subheader("💾 Download")
    
    if tier in ["intermediate", "advanced"]:
        st.download_button(
            label=f"📥 Download Video (720p)",
            data=b"",  # Placeholder
            file_name="lecture_720p.mp4",
            mime="video/mp4"
        )
    else:
        st.button("📥 Download Video", disabled=True, help="🔒 Download available in Intermediate tier ($247)")
        st.info("💡 Upgrade to Intermediate tier to download videos for offline viewing")
    
    # Transcript
    with st.expander("📝 View Transcript"):
        st.text_area("Transcript", "Attention mechanisms are...", height=200)

# Right: AI Tutor
with col3:
    st.subheader("🤖 AI Tutor")
    
    if tier == "basic":
        st.info("🔒 AI Tutor is available starting from **Intermediate tier ($247)**")
        st.button("Upgrade to Unlock", key="upgrade_ai_tutor")
    else:
        quota_used = 35 if tier == "intermediate" else -1
        quota_total = 50 if tier == "intermediate" else -1
        
        if tier == "intermediate":
            st.progress(quota_used / quota_total)
            st.caption(f"{quota_used}/{quota_total} questions used")
        else:
            st.success("✅ Unlimited questions")
        
        st.markdown("---")
        
        question = st.text_area("Ask a question:", placeholder="E.g., What is an attention mechanism?", height=100)
        
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button("Ask 🚀", use_container_width=True):
                if question:
                    st.success("✅ Question sent! (Demo mode)")
                else:
                    st.warning("Please enter a question")
        with col_y:
            if st.button("Clear 🗑️", use_container_width=True):
                st.rerun()

st.markdown("---")
st.caption("**Note**: This is a placeholder implementation. See documentation for full implementation details.")
