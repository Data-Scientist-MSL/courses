#!/usr/bin/env python3
"""
Intermediate Tier Demo - CoursePlayerApp

This demo shows the experience for Intermediate tier users:
- Interactive notebooks (JupyterLite)
- AI Tutor with 50 questions/month quota
- Download videos and slides
- Certificate generation

Run: streamlit run intermediate_tier_demo.py
"""

import streamlit as st
from datetime import datetime

# Mock CoursesGTM Client for demo
class MockGTMClient:
    """Mock CoursesGTM client for Intermediate tier demo"""
    
    @staticmethod
    def get_user_tier() -> str:
        return "intermediate"
    
    @staticmethod
    def can_use_feature(feature: str) -> bool:
        """Intermediate tier features"""
        intermediate_features = [
            "video_streaming", "video_download", "video_transcript",
            "slide_view", "slide_download",
            "notebook_view", "notebook_execution", "notebook_download",
            "ai_tutor", "ai_tutor_quota",
            "quiz_access", "quiz_analytics",
            "progress_tracking", "progress_analytics",
            "certificate_generation",
            "datasets", "code_review"
        ]
        return feature in intermediate_features
    
    @staticmethod
    def get_ai_tutor_usage() -> dict:
        """Get AI tutor quota status"""
        return {
            "used": 32,
            "limit": 50,
            "remaining": 18
        }


def render_tier_badge():
    """Render Intermediate tier badge"""
    st.markdown(
        '<span style="background-color:#3b82f6; color:white; '
        'padding:4px 12px; border-radius:12px; font-size:14px;">'
        '🔵 AI Practitioner • BEST VALUE</span>',
        unsafe_allow_html=True
    )


def render_video_player():
    """Render video player with download capability"""
    st.subheader("📹 Video Lesson")
    
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")
    
    st.caption("⏱️ 5:30 / 10:00")
    
    # Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("⏸ Pause")
    with col2:
        playback_speed = st.selectbox("Speed", ["0.5x", "1x", "1.5x", "2x"], index=1)
    with col3:
        if st.button("⬇️ Download"):
            st.success("Downloading video... (Demo)")
    with col4:
        if st.checkbox("Show Transcript"):
            st.text_area("Transcript", "This is the video transcript...", height=100)


def render_interactive_notebook():
    """Render interactive notebook with JupyterLite"""
    st.subheader("🧪 Interactive Lab: Pandas Basics")
    
    st.success("✨ **Interactive Mode** - You can run and edit code!")
    
    # Mock JupyterLite interface
    code = st.text_area(
        "Python Code",
        value="""import pandas as pd

# Create a DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})

print(df)
print(f"\\nAverage age: {df['age'].mean()}")""",
        height=200
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ Run Code"):
            st.code("""
      name  age     city
0    Alice   25      NYC
1      Bob   30       LA
2  Charlie   35  Chicago

Average age: 30.0
            """)
    with col2:
        if st.button("⬇️ Download Notebook"):
            st.success("Downloading notebook... (Demo)")
    with col3:
        if st.button("🔄 Reset"):
            st.info("Notebook reset to original state")
    
    st.info("💡 Upgrade to Advanced for full JupyterLab with GPU access")


def render_ai_tutor():
    """Render AI Tutor with quota"""
    st.subheader("🤖 AI Tutor")
    
    # Quota display
    usage = MockGTMClient.get_ai_tutor_usage()
    st.progress(usage['used'] / usage['limit'])
    st.caption(f"Questions remaining: {usage['remaining']}/{usage['limit']} this month (Resets: Feb 1)")
    
    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hi! I'm your AI tutor. Ask me anything about the course!"}
        ]
    
    # Display chat
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Input
    if prompt := st.chat_input("Ask a question..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Mock AI response
        response = f"Great question about '{prompt}'! Based on the course materials, " \
                  f"here's what you need to know... (This is a demo response)"
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
    
    st.info("💡 Upgrade to Advanced for unlimited AI Tutor questions with better model (llama3.1:8b)")


def render_certificates():
    """Show certificate generation"""
    st.subheader("📜 Your Certificates")
    
    st.success("✅ **Course Completed!** You've earned a certificate.")
    
    # Certificate preview
    st.image("https://via.placeholder.com/800x600/3b82f6/ffffff?text=Certificate+of+Completion", 
             caption="Certificate Preview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬇️ Download PDF"):
            st.success("Downloading certificate... (Demo)")
    with col2:
        if st.button("🔗 Verify"):
            st.info("Verification URL: https://gai-observe.online/verify/INT-CERT-12345")
    with col3:
        if st.button("📱 Share on LinkedIn"):
            st.success("Opening LinkedIn share... (Demo)")
    
    st.info("💡 Upgrade to Advanced for professionally signed certificates")


def main():
    """Main app"""
    st.set_page_config(
        page_title="CoursePlayerApp - Intermediate Tier Demo",
        page_icon="🎓",
        layout="wide"
    )
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎓 CoursePlayerApp")
        st.caption("Data Science 101 - Lesson 5: Advanced Pandas")
    with col2:
        render_tier_badge()
    
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.header("📚 Course Progress")
        st.progress(0.8)
        st.caption("80% Complete • 4 of 5 lessons")
        
        st.divider()
        
        st.metric("Learning Streak", "12 days", "🔥")
        st.metric("AI Questions Used", "32/50", "-18")
        st.metric("Quiz Average", "92%", "+5%")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📹 Video",
        "🧪 Interactive Lab",
        "🤖 AI Tutor",
        "📜 Certificates"
    ])
    
    with tab1:
        render_video_player()
    
    with tab2:
        render_interactive_notebook()
    
    with tab3:
        render_ai_tutor()
    
    with tab4:
        render_certificates()
    
    # Footer
    st.divider()
    st.markdown("""
    ### 🎉 Enjoying Intermediate Tier?
    
    **Upgrade to Advanced** for even more features:
    - 🔓 Unlimited AI Tutor
    - 🎮 GPU-powered notebooks
    - 📊 Production-grade datasets
    - 👨‍💻 Manual code review
    - 📦 Offline course packages
    
    **Only $250 more per year** → [Upgrade Now](#)
    """)


if __name__ == "__main__":
    main()
