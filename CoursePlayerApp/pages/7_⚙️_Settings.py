"""
CoursePlayerApp - Settings Page

This page displays user settings with tabs for:
- Profile information
- Subscription & tier management
- Notification preferences
- Accessibility settings
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Settings - CoursePlayerApp",
    page_icon="⚙️",
    layout="wide"
)

# Page content
st.title("⚙️ Settings")

st.info("""
**📋 This is a placeholder page**

This page will display:
- Profile information (read-only)
- Current tier and upgrade options
- Notification preferences
- Accessibility settings (high contrast, large text, dyslexia font, etc.)

See `docs/courseplayerapp/UI_UX_DESIGN.md` for full specifications.
""")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "💳 Subscription", "🔔 Notifications", "♿ Accessibility"])

with tab1:
    st.subheader("Profile Information")
    
    st.text_input("Email", value="student@example.com", disabled=True)
    st.text_input("User ID", value="user_12345", disabled=True)
    
    st.caption("Profile information is managed by your license key and cannot be edited here.")
    
    st.markdown("---")
    
    st.button("🚪 Logout", use_container_width=True)

with tab2:
    st.subheader("Subscription & Tier")
    
    # Get current tier
    tier = st.session_state.get('tier', 'basic')
    
    st.info(f"**Current Tier:** {tier.title()}")
    
    # Tier benefits
    st.markdown("**Your Benefits:**")
    
    if tier == 'basic':
        st.markdown("""
        - ✅ Access to 5 foundational courses
        - ✅ Video streaming (480p)
        - ✅ View slides (no export)
        - ✅ Read-only labs
        - ❌ No AI Tutor
        - ✅ Basic progress tracking
        """)
    elif tier == 'intermediate':
        st.markdown("""
        - ✅ Access to 8 courses
        - ✅ Video streaming + download (720p)
        - ✅ Slides export (PDF)
        - ✅ Interactive labs
        - ✅ AI Tutor (50 questions/month)
        - ✅ Advanced progress tracking
        """)
    else:  # advanced
        st.markdown("""
        - ✅ Access to ALL 9 courses
        - ✅ Video streaming + download (1080p)
        - ✅ Slides export (PDF + PPTX)
        - ✅ Full lab access
        - ✅ AI Tutor (unlimited)
        - ✅ Detailed analytics + heatmap
        - ✅ Premium blockchain certificates
        - ✅ Priority support
        """)
    
    # Upgrade section
    if tier != 'advanced':
        st.markdown("---")
        st.subheader("🚀 Upgrade Your Tier")
        
        if tier == 'basic':
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Intermediate - $247")
                st.write("✅ 8 courses")
                st.write("✅ 720p downloads")
                st.write("✅ AI Tutor (50 Q/month)")
                st.write("✅ Interactive labs")
                st.button("Upgrade to Intermediate", key="upgrade_int", use_container_width=True)
            
            with col2:
                st.markdown("### Advanced - $497")
                st.write("✅ All 9 courses")
                st.write("✅ 1080p downloads")
                st.write("✅ Unlimited AI Tutor")
                st.write("✅ Blockchain certificates")
                st.button("Upgrade to Advanced", key="upgrade_adv", use_container_width=True, type="primary")
        
        elif tier == 'intermediate':
            st.markdown("### Advanced - $497")
            st.write("✅ All 9 courses")
            st.write("✅ 1080p video quality")
            st.write("✅ Unlimited AI Tutor")
            st.write("✅ Blockchain-verified certificates")
            st.write("✅ Detailed analytics")
            st.button("Upgrade to Advanced", key="upgrade_adv2", use_container_width=True, type="primary")

with tab3:
    st.subheader("Notification Preferences")
    
    email_notifications = st.checkbox("Email notifications", value=True)
    course_updates = st.checkbox("Course content updates", value=True)
    certificate_alerts = st.checkbox("Certificate earned alerts", value=True)
    weekly_summary = st.checkbox("Weekly progress summary", value=False)
    
    st.markdown("---")
    
    if st.button("💾 Save Preferences", type="primary"):
        st.success("✅ Preferences saved!")

with tab4:
    st.subheader("♿ Accessibility Settings")
    
    st.markdown("**Visual**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        high_contrast = st.checkbox("High contrast mode")
        large_text = st.checkbox("Large text")
        dyslexia_font = st.checkbox("Dyslexia-friendly font (OpenDyslexic)")
    
    with col2:
        reduce_motion = st.checkbox("Reduce motion")
        focus_indicators = st.checkbox("Enhanced focus indicators", value=True)
    
    st.markdown("---")
    st.markdown("**Audio & Video**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        captions_default = st.checkbox("Enable captions by default", value=True)
        caption_size = st.select_slider(
            "Caption size",
            options=["Small", "Medium", "Large", "Extra Large"],
            value="Medium"
        )
    
    with col2:
        audio_descriptions = st.checkbox("Audio descriptions")
        autoplay_videos = st.checkbox("Autoplay videos")
    
    st.markdown("---")
    st.markdown("**Keyboard & Navigation**")
    
    keyboard_shortcuts = st.checkbox("Enable keyboard shortcuts", value=True)
    
    if keyboard_shortcuts:
        if st.button("⌨️ View Keyboard Shortcuts"):
            with st.expander("Keyboard Shortcuts", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    **Video Player**
                    - `Space` / `K`: Play/Pause
                    - `L` / `→`: Forward 10s
                    - `J` / `←`: Backward 10s
                    - `↑` / `↓`: Volume
                    - `F`: Fullscreen
                    """)
                
                with col2:
                    st.markdown("""
                    **Navigation**
                    - `N`: Next module
                    - `P`: Previous module
                    - `Ctrl + K`: Search
                    - `Ctrl + /`: AI Tutor
                    """)
    
    st.markdown("---")
    
    if st.button("💾 Save Accessibility Settings", type="primary"):
        st.success("✅ Accessibility settings saved!")
        st.balloons()
