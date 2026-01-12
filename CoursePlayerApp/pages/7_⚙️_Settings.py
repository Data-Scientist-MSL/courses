"""
CoursePlayerApp - Settings

User preferences and account management.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Settings - GAI-Observe Academy",
    page_icon="⚙️",
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
st.title("⚙️ Settings")
st.markdown("---")

# Profile section
st.subheader("👤 Profile")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Email", value=email, disabled=True)

with col2:
    st.text_input("User ID", value=user_id, disabled=True)

st.markdown("---")

# Subscription section
st.subheader("💳 Subscription")

col1, col2 = st.columns([2, 1])

with col1:
    tier_colors = {"basic": "gray", "intermediate": "blue", "advanced": "gold"}
    st.markdown(f"**Current Tier:** :{tier_colors[tier]}[{tier.title()}]")
    st.caption("License Expires: 2027-01-12")

with col2:
    if tier != "advanced":
        next_tier = "Intermediate" if tier == "basic" else "Advanced"
        price = "$247" if tier == "basic" else "$497"
        
        if st.button(f"⬆️ Upgrade to {next_tier} ({price})", type="primary", use_container_width=True):
            st.toast(f"Redirecting to upgrade page...")

st.markdown("---")

# Preferences section
st.subheader("🔔 Preferences")

col1, col2 = st.columns(2)

with col1:
    email_notifications = st.checkbox("Email notifications", value=True)
    weekly_report = st.checkbox("Weekly progress report", value=False)
    auto_resume = st.checkbox("Auto-resume videos", value=True)

with col2:
    course_reminders = st.checkbox("Course completion reminders", value=True)
    achievement_alerts = st.checkbox("Achievement notifications", value=True)
    community_updates = st.checkbox("Community updates", value=False)

st.markdown("---")

# Accessibility section
st.subheader("♿ Accessibility")

col1, col2 = st.columns(2)

with col1:
    high_contrast = st.checkbox("High contrast mode", value=False)
    dyslexic_font = st.checkbox("Dyslexia-friendly font (OpenDyslexic)", value=False)
    text_to_speech = st.checkbox("Enable text-to-speech for course content", value=False)

with col2:
    caption_lang = st.selectbox("Caption Language", ["English", "Spanish", "French", "German", "Chinese"])
    font_size = st.slider("Interface font size", 12, 20, 14)

st.markdown("---")

# Advanced tier caption customization
if tier == "advanced":
    st.subheader("🎨 Caption Customization (Advanced Tier)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        caption_size = st.slider("Caption font size", 12, 24, 16)
    
    with col2:
        caption_color = st.color_picker("Text color", "#FFFFFF")
    
    with col3:
        caption_bg = st.color_picker("Background", "#000000")
    
    with col4:
        caption_opacity = st.slider("BG opacity", 0.0, 1.0, 0.75)

st.markdown("---")

# Save and logout buttons
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        st.success("✅ Settings saved successfully!")

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        # Clear session
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        st.success("✅ Logged out successfully")
        st.balloons()
        
        import time
        time.sleep(2)
        st.switch_page("Home.py")

st.markdown("---")
st.caption("**Note**: This is a placeholder implementation. See documentation for full implementation details.")
