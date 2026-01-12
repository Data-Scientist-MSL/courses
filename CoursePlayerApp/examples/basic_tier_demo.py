#!/usr/bin/env python3
"""
Basic Tier Demo - CoursePlayerApp

This demo shows the experience for Basic tier users:
- Video streaming only (no downloads)
- View-only slides and notebooks
- Locked features with upgrade prompts
- No AI tutor access

Run: streamlit run basic_tier_demo.py
"""

import streamlit as st
from typing import Optional

# Mock CoursesGTM Client for demo
class MockGTMClient:
    """Mock CoursesGTM client for Basic tier demo"""
    
    @staticmethod
    def get_user_tier() -> str:
        return "basic"
    
    @staticmethod
    def can_use_feature(feature: str) -> bool:
        """Basic tier has limited features"""
        basic_features = [
            "video_streaming",
            "slide_view",
            "notebook_view",
            "quiz_access",
            "progress_tracking"
        ]
        return feature in basic_features
    
    @staticmethod
    def get_license_info() -> dict:
        return {
            "tier": "basic",
            "label": "Foundation Builder",
            "color": "#10b981",
            "expires_at": "2026-12-31"
        }


def render_tier_badge():
    """Render Basic tier badge"""
    st.markdown(
        '<span style="background-color:#10b981; color:white; '
        'padding:4px 12px; border-radius:12px; font-size:14px;">'
        '🟢 Foundation Builder</span>',
        unsafe_allow_html=True
    )


def render_upgrade_prompt(feature_name: str, target_tier: str, price: int):
    """Render upgrade prompt for locked features"""
    st.info(
        f"🔒 **{feature_name}** requires {target_tier} tier\n\n"
        f"Upgrade to unlock this feature for **${price}/year**"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Learn More"):
            st.session_state.show_pricing = True
    with col2:
        if st.button("Upgrade Now"):
            st.success("Redirecting to checkout... (Demo)")


def render_video_player():
    """Render video player with Basic tier limitations"""
    st.subheader("📹 Video Lesson")
    
    # Video streaming is available
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")
    
    st.caption("⏱️ 5:30 / 10:00")
    
    # Download button is locked
    col1, col2 = st.columns(2)
    with col1:
        st.button("⏸ Pause", key="pause")
    with col2:
        st.button("🔒 Download (Locked)", disabled=True, help="Upgrade to Intermediate")
    
    # Show upgrade prompt for download
    with st.expander("💡 Want to download videos?"):
        render_upgrade_prompt(
            "Video Downloads",
            "Intermediate",
            247
        )


def render_slides_viewer():
    """Render slides viewer - view only"""
    st.subheader("📊 Lesson Slides")
    
    st.image("https://via.placeholder.com/800x600/3b82f6/ffffff?text=Slide+1", use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.button("← Previous")
    with col2:
        st.text("Slide 1 of 10")
    with col3:
        st.button("Next →")
    
    # PDF export is locked
    st.button("🔒 Download as PDF (Locked)", disabled=True)
    
    with st.expander("💡 Want to download slides?"):
        render_upgrade_prompt(
            "Slide Downloads",
            "Intermediate",
            247
        )


def render_notebook_viewer():
    """Render notebook - static view only"""
    st.subheader("🧪 Lab: Pandas Basics")
    
    st.warning("📖 **View-Only Mode** - Upgrade to Intermediate for interactive notebooks")
    
    # Mock static notebook
    st.code("""
# Import pandas
import pandas as pd

# Create a DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})

print(df)
    """, language="python")
    
    st.text("Output:")
    st.code("""
      name  age     city
0    Alice   25      NYC
1      Bob   30       LA
2  Charlie   35  Chicago
    """)
    
    # Run button is locked
    st.button("🔒 Run Code (Locked)", disabled=True, help="Upgrade to Intermediate for interactive notebooks")
    
    with st.expander("💡 Want to run notebooks?"):
        render_upgrade_prompt(
            "Interactive Notebooks",
            "Intermediate",
            247
        )


def render_ai_tutor_locked():
    """Show AI tutor locked for Basic tier"""
    st.subheader("🤖 AI Tutor")
    
    st.warning("🔒 **AI Tutor is not available in Basic tier**")
    
    st.markdown("""
    **What you're missing:**
    - 50 AI tutor questions per month (Intermediate)
    - Unlimited questions (Advanced)
    - Context-aware answers from course materials
    - Code debugging help
    - Concept explanations
    """)
    
    render_upgrade_prompt(
        "AI Tutor Access",
        "Intermediate",
        247
    )


def main():
    """Main app"""
    st.set_page_config(
        page_title="CoursePlayerApp - Basic Tier Demo",
        page_icon="🎓",
        layout="wide"
    )
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎓 CoursePlayerApp")
        st.caption("Data Science 101 - Lesson 3: Pandas Basics")
    with col2:
        render_tier_badge()
    
    st.divider()
    
    # Sidebar navigation
    with st.sidebar:
        st.header("📚 Lessons")
        
        lessons = [
            ("✅", "1. Introduction", True),
            ("✅", "2. Python Setup", True),
            ("▶️", "3. Pandas Basics", True),  # Current
            ("⭕", "4. Data Visualization", False),
            ("⭕", "5. Statistics", False),
        ]
        
        for icon, lesson, completed in lessons:
            st.markdown(f"{icon} {lesson}")
        
        st.divider()
        st.subheader("🎯 Your Progress")
        st.progress(0.4)
        st.caption("40% Complete")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📹 Video", "📊 Slides", "🧪 Lab", "🤖 AI Tutor"])
    
    with tab1:
        render_video_player()
    
    with tab2:
        render_slides_viewer()
    
    with tab3:
        render_notebook_viewer()
    
    with tab4:
        render_ai_tutor_locked()
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("← Previous Lesson")
    with col2:
        if st.button("✓ Mark Complete"):
            st.success("Lesson marked complete!")
    with col3:
        st.button("Next Lesson →")
    
    # Pricing modal
    if st.session_state.get("show_pricing", False):
        with st.container():
            st.markdown("---")
            st.subheader("💎 Upgrade Your Plan")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Intermediate - AI Practitioner")
                st.markdown("**$247/year** 🏷️ BEST VALUE")
                st.markdown("""
                **Includes:**
                - ✅ Everything in Basic
                - ✅ Download videos & slides
                - ✅ Interactive notebooks (JupyterLite)
                - ✅ AI Tutor (50 questions/month)
                - ✅ Completion certificates
                - ✅ Course datasets
                """)
                st.button("Upgrade to Intermediate", key="upgrade_int")
            
            with col2:
                st.markdown("### Advanced - AI/ML Expert")
                st.markdown("**$497/year** 🏆 COMMERCIAL LICENSE")
                st.markdown("""
                **Includes:**
                - ✅ Everything in Intermediate
                - ✅ Unlimited AI Tutor
                - ✅ GPU-powered notebooks
                - ✅ Production datasets
                - ✅ Manual code review
                - ✅ Offline course packages
                """)
                st.button("Upgrade to Advanced", key="upgrade_adv")


if __name__ == "__main__":
    main()
