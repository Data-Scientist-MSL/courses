"""
CoursePlayerApp - Certificates

View and share earned certificates.
"""

import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="My Certificates - GAI-Observe Academy",
    page_icon="🎖️",
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
st.title("🎖️ My Certificates")
st.markdown("---")

# Mock certificate data
earned_certificates = [
    {
        "id": "cert-ai-02-2026",
        "course": "Machine Learning Fundamentals",
        "issue_date": "2026-01-05",
        "type": "Standard",
        "blockchain": False
    }
]

if earned_certificates:
    st.success(f"🎉 You've earned {len(earned_certificates)} certificate{'s' if len(earned_certificates) > 1 else ''}!")
    
    st.markdown("---")
    
    # Display certificates
    cols = st.columns(2)
    
    for i, cert in enumerate(earned_certificates):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"### 🎓 {cert['course']}")
                st.caption(f"Issued: {cert['issue_date']}")
                st.caption(f"Type: {cert['type']}")
                
                if cert['blockchain']:
                    st.success("✅ Blockchain verified")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        label="📥 Download",
                        data=b"",  # Placeholder
                        file_name=f"{cert['id']}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("📤 Share LinkedIn", key=f"linkedin_{cert['id']}", use_container_width=True):
                        st.toast("Opening LinkedIn share...")
                
                with col3:
                    if st.button("🔍 Verify", key=f"verify_{cert['id']}", use_container_width=True):
                        st.info(f"Verification link: https://verify.gai-observe.com/{cert['id']}")
                
                st.markdown("---")
else:
    st.info("You haven't earned any certificates yet.")

st.markdown("---")

# In-progress courses
st.subheader("🔓 Earn More Certificates")

in_progress_courses = [
    {
        "course": "NLP with Transformers",
        "progress": 67,
        "requirement": 80
    },
    {
        "course": "Deep Learning",
        "progress": 25,
        "requirement": 80
    }
]

for course in in_progress_courses:
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{course['course']}**")
            st.progress(course['progress'] / 100)
            st.caption(f"{course['progress']}% complete (need ≥{course['requirement']}% to take exam)")
        
        with col2:
            if course['progress'] >= course['requirement']:
                if st.button("Take Exam", key=f"exam_{course['course']}", type="primary", use_container_width=True):
                    st.toast("Launching certification exam...")
            else:
                st.button("Not Ready", disabled=True, use_container_width=True)
        
        st.markdown("---")

# Certificate types by tier
st.subheader("📜 Certificate Types")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Basic Tier")
    st.markdown("""
    - Standard design
    - PDF download
    - Online verification
    """)

with col2:
    st.markdown("### Intermediate Tier")
    st.markdown("""
    - Professional design
    - PDF download
    - Online verification
    - LinkedIn sharing
    """)

with col3:
    st.markdown("### Advanced Tier")
    st.markdown("""
    - Premium design
    - PDF download
    - **Blockchain verified** ⛓️
    - LinkedIn sharing
    - Custom branding
    """)

if tier != "advanced":
    st.info(f"💡 Upgrade to Advanced tier for blockchain-verified certificates!")

st.markdown("---")
st.caption("**Note**: This is a placeholder implementation. See documentation for full implementation details.")
