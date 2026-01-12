"""
Intermediate Tier Demo

This example demonstrates the CoursePlayerApp experience for Intermediate tier users.

Features Available:
- Everything in Basic
- Video downloads (720p)
- AI Tutor (50 questions/month)
- Interactive labs (JupyterLite)
- Verifiable certificates
- Full gamification (XP, levels, streaks)
- Advanced analytics

Run with: streamlit run examples/intermediate_tier_demo.py
"""

import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(
    page_title="CoursePlayerApp - Intermediate Tier Demo",
    page_icon="🟢",
    layout="wide"
)

# Simulate Intermediate tier session
if 'tier' not in st.session_state:
    st.session_state.tier = 'intermediate'
    st.session_state.user_name = 'Demo User'
    st.session_state.xp = 2450
    st.session_state.level = 12
    st.session_state.streak = 7
    st.session_state.ai_quota = 45  # 45/50 remaining
    st.session_state.chat_history = []

def render_header():
    """Render header with tier badge and stats"""
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title(f"🎓 Welcome back, {st.session_state.user_name}!")
    with col2:
        st.markdown("### 🟢 Intermediate")
        st.caption("$29/month")

def render_gamification():
    """Render gamification dashboard"""
    st.subheader("🎮 Your Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔥 Streak", f"{st.session_state.streak} days", "+1")
    with col2:
        st.metric("📈 Level", st.session_state.level, "+1")
    with col3:
        st.metric("💎 XP", st.session_state.xp, "+150")
    with col4:
        xp_to_next = (st.session_state.level + 1) * 1000 - st.session_state.xp
        st.metric("Next Level", f"{xp_to_next} XP", delta=None)

def render_ai_tutor():
    """Render AI tutor interface with quota"""
    st.subheader("🤖 AI Tutor")
    
    # Quota display
    quota = st.session_state.ai_quota
    total = 50
    st.progress(quota / total)
    st.caption(f"Questions remaining: {quota}/{total} (resets monthly)")
    
    # Chat interface
    with st.container():
        st.markdown("### Chat History")
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.write(msg['content'])
    
    # Input
    question = st.chat_input("Ask me anything about the course...")
    if question:
        if quota > 0:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': question
            })
            
            # Simulate AI response
            ai_response = f"""Great question about {question.split()[0] if question.split() else 'that topic'}! 

Here's a detailed explanation:

In machine learning, this concept is fundamental because it helps us understand how models learn from data. Let me break it down:

1. **Definition**: [Detailed explanation here]
2. **Example**: Consider a practical scenario...
3. **Code Sample**:
```python
import numpy as np
# Example code demonstrating the concept
def example_function(x):
    return x * 2
```

Would you like me to explain any specific part in more detail?"""
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': ai_response
            })
            
            # Decrement quota
            st.session_state.ai_quota -= 1
            st.experimental_rerun()
        else:
            st.error("Monthly quota exhausted!")
            st.info("Upgrade to Advanced for unlimited AI Tutor access!")

def render_video_with_download():
    """Render video player with download option"""
    st.subheader("📹 Machine Learning Algorithms")
    
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        quality = st.selectbox("Quality", ["auto", "480p", "720p"])
    with col2:
        speed = st.select_slider("Speed", options=[0.5, 0.75, 1.0, 1.25, 1.5, 2.0], value=1.0)
    with col3:
        if st.button("📥 Download (720p)"):
            st.success("Download started! Check your downloads folder.")

def render_interactive_lab():
    """Render interactive lab with JupyterLite"""
    st.subheader("🧪 Interactive Lab: Data Cleaning")
    
    st.success("✨ Interactive mode enabled!")
    
    # Simulated code cells
    st.markdown("**Cell 1: Import Libraries**")
    code1 = st.text_area(
        "Code:",
        value="import pandas as pd\nimport numpy as np\n\nprint('Libraries imported!')",
        height=100,
        key="cell1"
    )
    if st.button("▶️ Run", key="run1"):
        st.code("Libraries imported!", language="text")
    
    st.markdown("**Cell 2: Load Data**")
    code2 = st.text_area(
        "Code:",
        value="df = pd.read_csv('data.csv')\nprint(df.head())",
        height=80,
        key="cell2"
    )
    if st.button("▶️ Run", key="run2"):
        st.dataframe({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9]
        })
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("💾 Save Progress")
    with col2:
        st.button("📥 Export as HTML")

def render_certificate():
    """Render certificate page"""
    st.subheader("📜 Your Certificates")
    
    with st.container():
        st.markdown("### Machine Learning Fundamentals")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("**Completed:** January 15, 2024")
            st.write("**Score:** 92%")
            st.write("✅ Verified • Certificate ID: ML-2024-001234")
        with col2:
            st.button("📥 Download PDF")
            st.button("🔗 Share on LinkedIn")
    
    st.info("💡 Tip: Upgrade to Advanced for professionally signed certificates with digital signatures!")

def main():
    """Main application"""
    render_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Navigation")
        page = st.radio(
            "Go to:",
            ["Home", "AI Tutor", "Video Player", "Interactive Lab", "Certificates"]
        )
    
    # Page routing
    if page == "Home":
        st.markdown("---")
        render_gamification()
        
        st.markdown("---")
        st.subheader("📚 Continue Learning")
        st.write("**Course:** Machine Learning Fundamentals")
        st.progress(0.65)
        st.write("65% Complete")
        
    elif page == "AI Tutor":
        st.markdown("---")
        render_ai_tutor()
        
    elif page == "Video Player":
        st.markdown("---")
        render_video_with_download()
        
    elif page == "Interactive Lab":
        st.markdown("---")
        render_interactive_lab()
        
    elif page == "Certificates":
        st.markdown("---")
        render_certificate()
    
    # Footer
    st.markdown("---")
    st.caption("CoursePlayerApp - Intermediate Tier Demo | © 2024 GAI-Observe")

if __name__ == "__main__":
    main()
