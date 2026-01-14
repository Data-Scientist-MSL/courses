"""
CoursePlayerApp - Certificates Page

This page displays the certificate gallery with:
- Certificate grid view
- Download PDF functionality
- Share to LinkedIn
- Blockchain verification badge (Advanced)
- Verification links
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Certificates - CoursePlayerApp",
    page_icon="🎖️",
    layout="wide"
)

# Page content
st.title("🎖️ My Certificates")

st.info("""
**📋 This is a placeholder page**

This page will display:
- Certificate gallery (grid view)
- Download PDF button
- Share to LinkedIn integration
- Blockchain verification badge (Advanced tier)
- Verification links
- Certificate details (course, date, score)

See `docs/courseplayerapp/UI_UX_DESIGN.md` for full specifications.
""")

# Check if user has certificates
has_certificates = True  # This would check actual user data

if not has_certificates:
    st.info("🎯 No certificates yet. Complete a course to earn your first certificate!")
    st.button("📚 Browse Courses")
else:
    st.markdown("---")
    
    # Certificate grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://via.placeholder.com/300x400", use_column_width=True)
        st.markdown("**Introduction to Artificial Intelligence**")
        st.caption("Issued: January 15, 2026")
        st.caption("Score: 92%")
        
        # Blockchain badge (Advanced tier)
        tier = st.session_state.get('tier', 'basic')
        if tier == 'advanced':
            st.success("⛓️ Blockchain Verified")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.button("📥 Download", key="dl1", use_container_width=True)
        with col_b:
            st.button("🔗 Share", key="share1", use_container_width=True)
    
    with col2:
        st.image("https://via.placeholder.com/300x400", use_column_width=True)
        st.markdown("**Machine Learning Basics**")
        st.caption("Issued: December 20, 2025")
        st.caption("Score: 88%")
        
        if tier == 'advanced':
            st.success("⛓️ Blockchain Verified")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.button("📥 Download", key="dl2", use_container_width=True)
        with col_b:
            st.button("🔗 Share", key="share2", use_container_width=True)
    
    with col3:
        st.image("https://via.placeholder.com/300x400", use_column_width=True, alpha_channel="RGBA")
        st.markdown("**Course In Progress**")
        st.caption("NLP with Transformers")
        st.caption("Progress: 67%")
        st.info("Complete the course to earn your certificate")
        st.button("Continue Learning", key="continue", type="primary", use_container_width=True)

    st.markdown("---")
    
    st.subheader("Certificate Verification")
    st.write("""
    All certificates can be verified online. Each certificate has a unique ID 
    that can be checked at: https://verify.gai-observe.com
    """)
    
    if tier == 'advanced':
        st.success("""
        **Blockchain Verification** ⛓️
        
        Your certificates are also verified on the Polygon blockchain, 
        providing tamper-proof, decentralized verification.
        """)
