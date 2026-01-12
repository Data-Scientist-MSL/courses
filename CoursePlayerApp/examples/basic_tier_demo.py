"""
Basic Tier Demo

This example demonstrates the CoursePlayerApp experience for Basic tier users.

Features Available:
- Video streaming (auto quality only)
- View-only labs
- Basic quizzes
- Simple progress tracking

Features Locked:
- AI Tutor
- Video downloads
- Interactive labs
- Certificates
- Advanced analytics
"""

import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(
    page_title="CoursePlayerApp - Basic Tier Demo",
    page_icon="🎓",
    layout="wide"
)

# Simulate Basic tier session
if 'tier' not in st.session_state:
    st.session_state.tier = 'basic'
    st.session_state.user_name = 'Demo User'
    st.session_state.course_id = 'ml-fundamentals'
    st.session_state.progress = 15  # 15% complete

def render_header():
    """Render page header with tier badge"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"🎓 Welcome back, {st.session_state.user_name}!")
    with col2:
        st.markdown("### 🔵 Basic Tier")
        st.caption("Free Plan")

def render_video_player():
    """Render basic video player"""
    st.subheader("📹 Introduction to Machine Learning")
    
    # Simulated video player
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("Quality: Auto")  # No manual selection
    with col2:
        st.caption("Speed: 1x")  # No speed control
    with col3:
        # Download button disabled
        st.button("📥 Download 🔒", disabled=True, 
                  help="Upgrade to Intermediate to download videos")

def render_course_progress():
    """Render basic progress tracking"""
    st.subheader("📊 Your Progress")
    
    progress = st.session_state.progress
    st.progress(progress / 100)
    st.metric("Course Completion", f"{progress}%")
    
    st.info("🚀 Upgrade to Intermediate for detailed analytics, XP tracking, and achievement system!")

def render_locked_features():
    """Show locked features with upgrade prompts"""
    st.subheader("🔒 Unlock Premium Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🤖 AI Tutor
        Get instant help from our AI-powered tutor.
        
        **Available in**: Intermediate & Advanced
        
        - 50 questions/month (Intermediate)
        - Unlimited questions (Advanced)
        - Context-aware responses
        - Code examples
        """)
        if st.button("Try AI Tutor"):
            st.warning("Upgrade to Intermediate to unlock AI Tutor!")
    
    with col2:
        st.markdown("""
        ### 📜 Certificates
        Earn verifiable completion certificates.
        
        **Available in**: Intermediate & Advanced
        
        - PDF certificates
        - LinkedIn integration
        - QR code verification
        - Digital signatures (Advanced)
        """)
        if st.button("View Certificates"):
            st.warning("Complete courses and upgrade to earn certificates!")

def render_quiz():
    """Render basic quiz"""
    st.subheader("📝 Quiz: Machine Learning Basics")
    
    st.write("**Question 1:** What is machine learning?")
    q1 = st.radio(
        "Select your answer:",
        [
            "A) Programming computers to learn from data",
            "B) Teaching machines to think like humans",
            "C) Building physical robots",
            "D) Writing code manually"
        ],
        key="q1"
    )
    
    st.write("**Question 2:** Which is a supervised learning task?")
    q2 = st.radio(
        "Select your answer:",
        [
            "A) Clustering customers by behavior",
            "B) Predicting house prices",
            "C) Discovering hidden patterns",
            "D) Dimensionality reduction"
        ],
        key="q2"
    )
    
    if st.button("Submit Quiz"):
        score = 0
        if "A)" in q1:
            score += 50
            st.success("Question 1: Correct! ✅")
        else:
            st.error("Question 1: Incorrect ❌")
        
        if "B)" in q2:
            score += 50
            st.success("Question 2: Correct! ✅")
        else:
            st.error("Question 2: Incorrect ❌")
        
        st.metric("Your Score", f"{score}%")
        
        if score == 100:
            st.balloons()
            st.success("Perfect score! Well done! 🎉")

def render_lab_viewer():
    """Render view-only lab"""
    st.subheader("🧪 Lab: Data Preprocessing (View Only)")
    
    st.info("🚀 Upgrade to Intermediate to run code interactively!")
    
    # Static code view
    st.code("""
# Data Preprocessing Lab

import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('data.csv')
print(df.head())

# Handle missing values
df = df.dropna()

# Feature scaling
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

print("Preprocessing complete!")
    """, language="python")
    
    st.caption("Output would appear here in interactive mode.")

def main():
    """Main application"""
    render_header()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")
        page = st.radio(
            "Go to:",
            ["Home", "Learn", "Quiz", "Lab", "Locked Features"]
        )
    
    # Page routing
    if page == "Home":
        st.markdown("---")
        render_course_progress()
        
        st.markdown("---")
        st.subheader("🎯 Quick Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("🎓 Continue Learning")
        with col2:
            st.button("📝 Take Quiz")
        with col3:
            st.button("📊 View Progress")
        
        st.markdown("---")
        st.subheader("📚 Course: Machine Learning Fundamentals")
        st.write("**Current Module:** Introduction to ML")
        st.write("**Lessons Completed:** 3 / 24")
        st.write("**Next Lesson:** Supervised Learning")
        
    elif page == "Learn":
        st.markdown("---")
        render_video_player()
        
        st.markdown("---")
        st.subheader("📄 Lesson Notes")
        st.write("""
        **Key Concepts:**
        - Machine learning enables computers to learn from data
        - Supervised learning uses labeled data
        - Unsupervised learning finds patterns in unlabeled data
        """)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.button("⬅️ Previous Lesson")
        with col2:
            if st.button("✅ Mark Complete"):
                st.session_state.progress += 4
                st.success("Lesson marked complete!")
                st.experimental_rerun()
        with col3:
            st.button("Next Lesson ➡️")
    
    elif page == "Quiz":
        st.markdown("---")
        render_quiz()
    
    elif page == "Lab":
        st.markdown("---")
        render_lab_viewer()
    
    elif page == "Locked Features":
        st.markdown("---")
        render_locked_features()
        
        st.markdown("---")
        st.subheader("⭐ Compare Plans")
        
        comp_col1, comp_col2, comp_col3 = st.columns(3)
        
        with comp_col1:
            st.markdown("### 🔵 Basic")
            st.markdown("**Free**")
            st.markdown("""
            - Video streaming
            - Basic quizzes
            - View-only labs
            - Simple progress
            """)
            st.success("Current Plan")
        
        with comp_col2:
            st.markdown("### 🟢 Intermediate")
            st.markdown("**$29/month**")
            st.markdown("""
            - Everything in Basic
            - ✅ AI Tutor (50 q/mo)
            - ✅ Video downloads
            - ✅ Interactive labs
            - ✅ Certificates
            - ✅ Analytics
            """)
            st.button("Upgrade to Intermediate", key="upgrade_int", use_container_width=True)
        
        with comp_col3:
            st.markdown("### ⭐ Advanced")
            st.markdown("**$79/month**")
            st.markdown("""
            - Everything in Intermediate
            - ✅ Unlimited AI Tutor
            - ✅ Offline mode
            - ✅ Full JupyterLab
            - ✅ Code review
            - ✅ Predictions
            """)
            st.button("Upgrade to Advanced", key="upgrade_adv", use_container_width=True)

    # Footer
    st.markdown("---")
    st.caption("CoursePlayerApp - Basic Tier Demo | © 2024 GAI-Observe")

if __name__ == "__main__":
    main()
