"""
CoursePlayerApp - Home (Login Page)

This is the entry point for the application. Users authenticate using their license key.
"""

import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="GAI-Observe Academy - Login",
    page_icon="🎓",
    layout="centered"
)

# Check if already authenticated
if st.session_state.get("authenticated"):
    st.switch_page("pages/1_🏠_Dashboard.py")

# Header
st.title("🎓 GAI-Observe Academy")
st.markdown("### Welcome to Your Learning Journey!")
st.markdown("---")

# Login form
with st.container():
    st.markdown("#### Login with Your License Key")
    
    license_key = st.text_input(
        "License Key",
        type="password",
        placeholder="XXXX-XXXX-XXXX-XXXX",
        help="Enter the license key you received after purchase"
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("🔐 Login", type="primary", use_container_width=True):
            if license_key:
                with st.spinner("Validating license..."):
                    # TODO: Implement actual authentication
                    # from utils.auth import authenticate
                    # success = authenticate(license_key)
                    
                    # Mock authentication for demo
                    time.sleep(1)
                    st.session_state["authenticated"] = True
                    st.session_state["user_id"] = "demo-user-123"
                    st.session_state["email"] = "demo@example.com"
                    st.session_state["tier"] = "intermediate"
                    
                    st.success("✅ Login successful!")
                    time.sleep(1)
                    st.switch_page("pages/1_🏠_Dashboard.py")
            else:
                st.error("Please enter your license key")
    
    with col2:
        if st.button("🔄 Clear", use_container_width=True):
            st.rerun()

st.markdown("---")

# Help section
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Don't have a license?**")
    st.markdown("[💳 Purchase Now](https://payment.gai-observe.com)")

with col2:
    st.markdown("**Need help?**")
    st.markdown("[📧 Contact Support](mailto:support@gai-observe.com)")

# Expandable help
with st.expander("❓ Troubleshooting"):
    st.markdown("""
    **License key not working?**
    - Verify you entered it correctly (hyphens are optional)
    - Check your purchase confirmation email
    - Ensure your license hasn't expired
    - Contact support if the issue persists
    
    **First time user?**
    - Your license key was sent to your email after purchase
    - Make sure to check your spam folder
    - Each license key can only be used on one device at a time
    """)

# Footer
st.markdown("---")
st.caption("© 2026 GAI-Observe Academy. All rights reserved.")
st.caption("**Note**: This is a placeholder implementation. See documentation for full implementation details.")
