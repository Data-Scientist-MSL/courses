# CoursePlayerApp Feature Gating Specification

## Overview

Feature gating is the core mechanism that differentiates the learning experience across EdGuide's three pricing tiers: **Basic ($97)**, **Intermediate ($247)**, and **Advanced ($497)**. This document defines exactly which features are available at each tier and how they are enforced in the UI and backend.

## Pricing Tier Structure

### Basic Tier - $97 (Foundation)
**Target Audience**: Students who want to explore courses with minimal investment  
**Value Proposition**: Access to all course content in view-only mode with standard certificate

### Intermediate Tier - $247 (Professional)
**Target Audience**: Professionals who want hands-on practice and AI assistance  
**Value Proposition**: Interactive labs, video downloads, AI Tutor with quota, professional certificates

### Advanced Tier - $497 (Elite)
**Target Audience**: Serious learners who want unlimited access and premium features  
**Value Proposition**: Unlimited AI Tutor, 1080p downloads, blockchain certificates, priority support, community access

---

## Feature Matrix by Tier

### Video Features

| Feature | Basic | Intermediate | Advanced | Notes |
|---------|-------|--------------|----------|-------|
| **Stream Videos (Any Quality)** | ✅ | ✅ | ✅ | HLS adaptive streaming |
| **Playback Speed Control** | ✅ | ✅ | ✅ | 0.5x to 2x |
| **Subtitles/Captions** | ✅ | ✅ | ✅ | WebVTT format |
| **Bookmark/Resume** | ✅ | ✅ | ✅ | Auto-save position |
| **Download Video (720p)** | ❌ | ✅ | ✅ | Watermarked with user email |
| **Download Video (1080p)** | ❌ | ❌ | ✅ | Watermarked with user email |
| **Picture-in-Picture** | ✅ | ✅ | ✅ | Browser-dependent |
| **Chapter Markers** | ✅ | ✅ | ✅ | Jump to topics |
| **Quality Selector** | ✅ (stream only) | ✅ | ✅ | Auto, 360p, 720p, 1080p |

**UI Implementation**:
```python
# Video player component
def render_video_player(video_id: str, user_tier: str):
    # Always show video player
    st.video(get_video_stream_url(video_id))
    
    # Show download button based on tier
    if user_tier in ["intermediate", "advanced"]:
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Download 720p",
                data=get_video_file(video_id, "720p"),
                file_name=f"{video_id}_720p.mp4"
            )
        with col2:
            if user_tier == "advanced":
                st.download_button(
                    "⬇️ Download 1080p",
                    data=get_video_file(video_id, "1080p"),
                    file_name=f"{video_id}_1080p.mp4"
                )
            else:
                st.button("🔒 Download 1080p (Advanced Only)", disabled=True)
                st.caption("💎 Upgrade to Advanced for 1080p downloads")
    else:
        st.info("🔒 Video downloads are locked. Upgrade to Intermediate to download videos (720p)")
```

---

### Slide Features

| Feature | Basic | Intermediate | Advanced | Notes |
|---------|-------|--------------|----------|-------|
| **View Slides (In Browser)** | ✅ | ✅ | ✅ | Read-only viewer |
| **Search Slides** | ✅ | ✅ | ✅ | Full-text search |
| **Export Slides (PDF)** | ❌ | ✅ | ✅ | Watermarked |
| **Export Slides (PPTX)** | ❌ | ❌ | ✅ | Editable format |
| **Print Slides** | ❌ | ✅ | ✅ | Via PDF export |

**UI Implementation**:
```python
def render_slide_viewer(slide_deck_id: str, user_tier: str):
    # Always show slide viewer
    render_slide_carousel(slide_deck_id)
    
    # Export options based on tier
    st.subheader("Export Options")
    
    if user_tier in ["intermediate", "advanced"]:
        st.download_button(
            "📄 Export as PDF",
            data=generate_pdf(slide_deck_id),
            file_name=f"{slide_deck_id}.pdf"
        )
        
        if user_tier == "advanced":
            st.download_button(
                "📊 Export as PPTX",
                data=generate_pptx(slide_deck_id),
                file_name=f"{slide_deck_id}.pptx"
            )
        else:
            st.button("🔒 Export as PPTX (Advanced Only)", disabled=True)
            st.caption("💎 Upgrade to Advanced for editable PowerPoint files")
    else:
        st.info("🔒 Slide exports are locked. Upgrade to Intermediate for PDF exports")
```

---

### Lab Features

| Feature | Basic | Intermediate | Advanced | Notes |
|---------|-------|--------------|----------|-------|
| **View Lab Instructions** | ✅ | ✅ | ✅ | Read instructions |
| **View Code (Read-Only)** | ✅ | ✅ | ✅ | Syntax-highlighted view |
| **Copy Code** | ✅ | ✅ | ✅ | Copy to clipboard |
| **Execute Code (Jupyter)** | ❌ | ✅ | ✅ | Interactive notebooks |
| **Execute Code (Terminal)** | ❌ | ✅ | ✅ | Web-based terminal |
| **File Upload/Download** | ❌ | ✅ | ✅ | To/from sandbox |
| **Package Installation** | ❌ | ✅ | ✅ | pip, conda, npm |
| **Save Workspace** | ❌ | ✅ | ✅ | Persist across sessions |
| **Sandbox Resources** | N/A | 2 CPU, 4GB RAM | 4 CPU, 8GB RAM | Resource allocation |

**UI Implementation**:
```python
def render_lab_environment(lab_id: str, user_tier: str):
    if user_tier == "basic":
        # View-only mode
        st.warning("🔒 Interactive lab execution is locked. You can view the code below.")
        st.info("💎 Upgrade to Intermediate to execute code and complete hands-on exercises")
        
        # Show read-only code viewer
        code = get_lab_code(lab_id)
        st.code(code, language="python")
        
        # Copy button
        st.button("📋 Copy Code", on_click=lambda: copy_to_clipboard(code))
        
    elif user_tier in ["intermediate", "advanced"]:
        # Interactive mode
        st.success("✅ Interactive lab environment enabled")
        
        # Embed JupyterLab or code editor
        render_jupyter_lab(
            lab_id=lab_id,
            user_id=st.session_state.user_id,
            resources={
                "cpu": 2 if user_tier == "intermediate" else 4,
                "memory": "4GB" if user_tier == "intermediate" else "8GB"
            }
        )
        
        # File operations
        col1, col2 = st.columns(2)
        with col1:
            uploaded_file = st.file_uploader("Upload to Sandbox")
        with col2:
            st.download_button("Download Workspace", data=export_workspace(lab_id))
```

---

### AI Tutor Features

| Feature | Basic | Intermediate | Advanced | Notes |
|---------|-------|--------------|----------|-------|
| **AI Tutor Access** | ❌ | ✅ (50 Q/month) | ✅ (Unlimited) | OLLAMA-powered |
| **Context-Aware Q&A** | ❌ | ✅ | ✅ | Knows current course/module |
| **Code Explanation** | ❌ | ✅ | ✅ | Explain code snippets |
| **Practice Problems** | ❌ | ✅ | ✅ | Generate exercises |
| **Study Tips** | ❌ | ✅ | ✅ | Learning strategies |
| **Quota Display** | N/A | ✅ | N/A (Unlimited) | Shows remaining questions |
| **Response Priority** | N/A | Standard | Priority | Faster response for Advanced |

**Quota Management**:
```python
class AITutorQuota:
    QUOTAS = {
        "basic": 0,          # Locked
        "intermediate": 50,  # Per month
        "advanced": float('inf')  # Unlimited
    }
    
    def __init__(self, user_id: str, tier: str):
        self.user_id = user_id
        self.tier = tier
        self.quota_limit = self.QUOTAS[tier]
        
    def get_usage(self) -> int:
        """Get number of questions used this month."""
        cache_key = f"ai_tutor_quota:{self.user_id}:{get_current_month()}"
        return int(redis_client.get(cache_key) or 0)
    
    def get_remaining(self) -> int:
        """Get remaining questions this month."""
        if self.tier == "advanced":
            return float('inf')
        return max(0, self.quota_limit - self.get_usage())
    
    def can_ask(self) -> bool:
        """Check if user can ask another question."""
        if self.tier == "basic":
            return False
        if self.tier == "advanced":
            return True
        return self.get_remaining() > 0
    
    def use_quota(self):
        """Increment usage counter."""
        if self.tier == "advanced":
            return  # No quota to track
        
        cache_key = f"ai_tutor_quota:{self.user_id}:{get_current_month()}"
        redis_client.incr(cache_key)
        # Set expiration to end of month
        redis_client.expireat(cache_key, get_end_of_month_timestamp())
```

**UI Implementation**:
```python
def render_ai_tutor_chat(user_tier: str):
    quota = AITutorQuota(st.session_state.user_id, user_tier)
    
    if user_tier == "basic":
        st.info("🔒 AI Tutor is locked")
        st.markdown("""
        **Unlock AI-Powered Learning Assistant:**
        - Get instant answers to your questions
        - Explain complex code and concepts
        - Generate practice problems
        - Receive personalized study tips
        """)
        st.button("💎 Upgrade to Intermediate (50 Q/month) - $247", on_click=redirect_to_upgrade)
        return
    
    # Show quota for Intermediate tier
    if user_tier == "intermediate":
        remaining = quota.get_remaining()
        used = quota.get_usage()
        
        st.metric(
            "AI Tutor Questions This Month",
            f"{used}/50",
            f"{remaining} remaining"
        )
        
        if remaining < 10:
            st.warning(f"⚠️ Only {remaining} questions remaining this month")
            st.info("💎 Upgrade to Advanced for unlimited AI Tutor access")
    
    elif user_tier == "advanced":
        st.success("✅ Unlimited AI Tutor Access")
    
    # Chat interface
    if quota.can_ask():
        user_question = st.text_input("Ask the AI Tutor:")
        if st.button("Send") and user_question:
            with st.spinner("Thinking..."):
                answer = ai_tutor.ask(
                    question=user_question,
                    context={
                        "course_id": st.session_state.current_course,
                        "module_id": st.session_state.current_module,
                        "video_timestamp": st.session_state.video_position
                    }
                )
                quota.use_quota()
                st.markdown(answer)
    else:
        st.error("❌ Monthly quota exceeded. Upgrade to Advanced for unlimited access.")
        st.button("💎 Upgrade to Advanced - $497", on_click=redirect_to_upgrade)
```

---

### Simulation Features

| Feature | Basic | Intermediate | Advanced | Notes |
|---------|-------|--------------|----------|-------|
| **View Simulation (Demo Mode)** | ✅ | ✅ | ✅ | Watch demo video |
| **Basic Simulations** | ❌ | ✅ | ✅ | Simple interactive sims |
| **Advanced Simulations** | ❌ | ❌ | ✅ | Complex multi-step sims |
| **Simulation Quota** | N/A | 10/month | Unlimited | Launches per month |
| **Simulation Analytics** | ❌ | ✅ | ✅ | Performance tracking |

---

### Certificate Features

| Feature | Basic | Intermediate | Advanced | Notes |
|---------|-------|--------------|----------|-------|
| **Course Completion Certificate** | ✅ | ✅ | ✅ | All tiers get certificate |
| **Certificate Template** | Standard | Professional | Premium | Design quality |
| **Download as PDF** | ✅ | ✅ | ✅ | Print-ready |
| **Share to LinkedIn** | ❌ | ✅ | ✅ | One-click share |
| **Digital Wallet (Apple/Google)** | ❌ | ✅ | ✅ | Add to wallet |
| **QR Code Verification** | ✅ | ✅ | ✅ | Public verification |
| **Blockchain Verification** | ❌ | ❌ | ✅ | Immutable proof |
| **Custom Branding** | ❌ | ❌ | ✅ | Add company logo |

**UI Implementation**:
```python
def render_certificate_display(certificate: Certificate, user_tier: str):
    # Show certificate image (tier-specific template)
    template = {
        "basic": "standard_template.png",
        "intermediate": "professional_template.png",
        "advanced": "premium_template.png"
    }[user_tier]
    
    st.image(generate_certificate_image(certificate, template))
    
    # Download PDF (all tiers)
    st.download_button(
        "📄 Download PDF",
        data=generate_certificate_pdf(certificate),
        file_name=f"certificate_{certificate.id}.pdf"
    )
    
    # LinkedIn share (Intermediate+)
    if user_tier in ["intermediate", "advanced"]:
        linkedin_url = generate_linkedin_share_url(certificate)
        st.link_button("🔗 Share on LinkedIn", linkedin_url)
        
        # Digital wallet (Intermediate+)
        st.download_button(
            "📱 Add to Apple Wallet",
            data=generate_apple_wallet_pass(certificate),
            file_name=f"certificate_{certificate.id}.pkpass"
        )
    else:
        st.button("🔒 Share on LinkedIn (Intermediate+)", disabled=True)
    
    # QR code verification (all tiers)
    verification_url = f"https://gai-observe.online/verify/{certificate.id}"
    st.image(generate_qr_code(verification_url))
    st.caption(f"Verify at: {verification_url}")
    
    # Blockchain verification (Advanced only)
    if user_tier == "advanced":
        st.success("✅ Blockchain Verified")
        st.code(certificate.blockchain_hash, language="text")
        st.link_button(
            "🔍 View on Blockchain",
            f"https://etherscan.io/tx/{certificate.blockchain_hash}"
        )
    else:
        st.info("💎 Upgrade to Advanced for blockchain-verified certificates")
```

---

### Progress Tracking & Analytics

| Feature | Basic | Intermediate | Advanced | Notes |
|---------|-------|--------------|----------|-------|
| **Basic Progress Bar** | ✅ | ✅ | ✅ | Course completion % |
| **Videos Watched Count** | ✅ | ✅ | ✅ | Simple counter |
| **Labs Completed Count** | ✅ | ✅ | ✅ | Simple counter |
| **Detailed Analytics Dashboard** | ❌ | ✅ | ✅ | Charts, graphs |
| **Time Spent Breakdown** | ❌ | ✅ | ✅ | Per module/topic |
| **Learning Velocity** | ❌ | ❌ | ✅ | Pace analysis |
| **Predictive Insights** | ❌ | ❌ | ✅ | AI-powered suggestions |
| **Comparison with Peers** | ❌ | ❌ | ✅ | Anonymous leaderboard |
| **Export Analytics Data** | ❌ | ❌ | ✅ | CSV/JSON export |

---

### Support Features

| Feature | Basic | Intermediate | Advanced | Notes |
|---------|-------|--------------|----------|-------|
| **Help Center Access** | ✅ | ✅ | ✅ | Self-service docs |
| **Email Support** | ✅ | ✅ | ✅ | 48-hour response |
| **Priority Email Support** | ❌ | ❌ | ✅ | 24-hour response |
| **Live Chat** | ❌ | ❌ | ✅ | Business hours |
| **1-on-1 Mentorship** | ❌ | ❌ | ✅ (1 session) | 30-min video call |

---

### Community & Extras

| Feature | Basic | Intermediate | Advanced | Notes |
|---------|-------|--------------|----------|-------|
| **Public Forum Access** | ✅ | ✅ | ✅ | Read-only for Basic |
| **Post in Forums** | ❌ | ✅ | ✅ | Ask questions |
| **Private Discord/Slack** | ❌ | ❌ | ✅ | Exclusive community |
| **Early Access to New Courses** | ❌ | ❌ | ✅ | 1-week early access |
| **Beta Features** | ❌ | ❌ | ✅ | Test new features first |
| **Course Completion Badges** | ✅ | ✅ | ✅ (Special) | Gamification |

---

## Implementation Guide

### Backend: Feature Gate Function

```python
# courseplayerapp/core/feature_gate.py

from typing import Dict, List, Optional
from enum import Enum

class Tier(str, Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Feature(str, Enum):
    # Video
    VIDEO_STREAMING = "video_streaming"
    VIDEO_DOWNLOAD_720P = "video_download_720p"
    VIDEO_DOWNLOAD_1080P = "video_download_1080p"
    
    # Slides
    SLIDE_VIEW = "slide_view"
    SLIDE_EXPORT_PDF = "slide_export_pdf"
    SLIDE_EXPORT_PPTX = "slide_export_pptx"
    
    # Labs
    LAB_VIEW = "lab_view"
    LAB_EXECUTION = "lab_execution"
    
    # AI Tutor
    AI_TUTOR_LIMITED = "ai_tutor_limited"
    AI_TUTOR_UNLIMITED = "ai_tutor_unlimited"
    
    # Simulations
    SIMULATION_BASIC = "simulation_basic"
    SIMULATION_ADVANCED = "simulation_advanced"
    
    # Certificates
    CERTIFICATE_STANDARD = "certificate_standard"
    CERTIFICATE_LINKEDIN = "certificate_linkedin"
    CERTIFICATE_BLOCKCHAIN = "certificate_blockchain"
    
    # Analytics
    ANALYTICS_BASIC = "analytics_basic"
    ANALYTICS_DETAILED = "analytics_detailed"
    ANALYTICS_INSIGHTS = "analytics_insights"
    
    # Support
    SUPPORT_BASIC = "support_basic"
    SUPPORT_PRIORITY = "support_priority"
    
    # Community
    COMMUNITY_ACCESS = "community_access"

# Feature access matrix
FEATURE_MATRIX: Dict[Feature, List[Tier]] = {
    # Video
    Feature.VIDEO_STREAMING: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.VIDEO_DOWNLOAD_720P: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.VIDEO_DOWNLOAD_1080P: [Tier.ADVANCED],
    
    # Slides
    Feature.SLIDE_VIEW: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.SLIDE_EXPORT_PDF: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.SLIDE_EXPORT_PPTX: [Tier.ADVANCED],
    
    # Labs
    Feature.LAB_VIEW: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.LAB_EXECUTION: [Tier.INTERMEDIATE, Tier.ADVANCED],
    
    # AI Tutor
    Feature.AI_TUTOR_LIMITED: [Tier.INTERMEDIATE],
    Feature.AI_TUTOR_UNLIMITED: [Tier.ADVANCED],
    
    # Simulations
    Feature.SIMULATION_BASIC: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.SIMULATION_ADVANCED: [Tier.ADVANCED],
    
    # Certificates
    Feature.CERTIFICATE_STANDARD: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.CERTIFICATE_LINKEDIN: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.CERTIFICATE_BLOCKCHAIN: [Tier.ADVANCED],
    
    # Analytics
    Feature.ANALYTICS_BASIC: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.ANALYTICS_DETAILED: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.ANALYTICS_INSIGHTS: [Tier.ADVANCED],
    
    # Support
    Feature.SUPPORT_BASIC: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.SUPPORT_PRIORITY: [Tier.ADVANCED],
    
    # Community
    Feature.COMMUNITY_ACCESS: [Tier.ADVANCED],
}

def can_access_feature(user_tier: str, feature: str) -> bool:
    """
    Check if a user tier has access to a specific feature.
    
    Args:
        user_tier: User's subscription tier (basic, intermediate, advanced)
        feature: Feature to check access for
    
    Returns:
        True if user has access, False otherwise
    """
    try:
        tier = Tier(user_tier.lower())
        feat = Feature(feature)
        return tier in FEATURE_MATRIX.get(feat, [])
    except (ValueError, KeyError):
        return False

def get_unlock_tier(feature: str) -> Optional[str]:
    """
    Get the minimum tier required to unlock a feature.
    
    Args:
        feature: Feature to check
    
    Returns:
        Tier name that unlocks the feature, or None if invalid
    """
    try:
        feat = Feature(feature)
        allowed_tiers = FEATURE_MATRIX.get(feat, [])
        if not allowed_tiers:
            return None
        
        # Return the lowest tier that has access
        tier_order = [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED]
        for tier in tier_order:
            if tier in allowed_tiers:
                return tier.value
    except ValueError:
        return None

def get_tier_features(tier: str) -> List[str]:
    """
    Get all features available for a specific tier.
    
    Args:
        tier: User tier (basic, intermediate, advanced)
    
    Returns:
        List of feature names available to this tier
    """
    try:
        tier_enum = Tier(tier.lower())
        features = []
        for feature, allowed_tiers in FEATURE_MATRIX.items():
            if tier_enum in allowed_tiers:
                features.append(feature.value)
        return features
    except ValueError:
        return []
```

### Frontend: Upgrade CTA Component

```python
# courseplayerapp/ui/components/upgrade_cta.py

import streamlit as st

def render_upgrade_cta(feature: str, current_tier: str):
    """
    Render an upgrade call-to-action for a locked feature.
    
    Args:
        feature: Name of the locked feature
        current_tier: User's current tier
    """
    from courseplayerapp.core.feature_gate import get_unlock_tier
    
    unlock_tier = get_unlock_tier(feature)
    
    if unlock_tier is None:
        return
    
    # Feature descriptions
    feature_descriptions = {
        "video_download_720p": "Download videos in 720p for offline viewing",
        "video_download_1080p": "Download videos in full 1080p HD quality",
        "ai_tutor_limited": "Get AI-powered answers to 50 questions per month",
        "ai_tutor_unlimited": "Ask unlimited questions to your AI Tutor",
        "lab_execution": "Execute code in interactive Jupyter notebooks",
        "slide_export_pdf": "Export slides as PDF documents",
        "slide_export_pptx": "Export slides as editable PowerPoint files",
        "certificate_linkedin": "Share your certificates directly to LinkedIn",
        "certificate_blockchain": "Get blockchain-verified certificates",
        "community_access": "Join our exclusive Discord/Slack community",
    }
    
    # Tier prices
    tier_prices = {
        "basic": "$97",
        "intermediate": "$247",
        "advanced": "$497"
    }
    
    description = feature_descriptions.get(feature, "Unlock premium features")
    price = tier_prices.get(unlock_tier, "")
    
    st.info(f"🔒 **{description}**")
    st.markdown(f"💎 **Upgrade to {unlock_tier.capitalize()} tier ({price}) to unlock this feature**")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("✨ Upgrade Now"):
            st.session_state.redirect_to = f"/upgrade?target_tier={unlock_tier}"
            st.rerun()
    with col2:
        if st.button("📊 Compare Plans"):
            st.session_state.redirect_to = "/pricing"
            st.rerun()
```

---

## Testing Strategy

### Unit Tests
```python
# tests/test_feature_gate.py

import pytest
from courseplayerapp.core.feature_gate import can_access_feature, get_unlock_tier

class TestFeatureGate:
    def test_basic_tier_video_streaming(self):
        assert can_access_feature("basic", "video_streaming") == True
    
    def test_basic_tier_video_download(self):
        assert can_access_feature("basic", "video_download_720p") == False
    
    def test_intermediate_tier_ai_tutor(self):
        assert can_access_feature("intermediate", "ai_tutor_limited") == True
        assert can_access_feature("intermediate", "ai_tutor_unlimited") == False
    
    def test_advanced_tier_all_features(self):
        assert can_access_feature("advanced", "video_download_1080p") == True
        assert can_access_feature("advanced", "ai_tutor_unlimited") == True
        assert can_access_feature("advanced", "certificate_blockchain") == True
    
    def test_unlock_tier_detection(self):
        assert get_unlock_tier("video_download_720p") == "intermediate"
        assert get_unlock_tier("video_download_1080p") == "advanced"
        assert get_unlock_tier("video_streaming") == "basic"
```

---

## Migration & Rollout Plan

### Phase 1: Grandfather Existing Users
- All existing users default to **Intermediate** tier
- 30-day grace period to choose tier

### Phase 2: New User Onboarding
- New users select tier during signup
- 7-day free trial of **Intermediate** tier
- Downgrade to **Basic** or upgrade to **Advanced** after trial

### Phase 3: Upgrade Flow
- In-app upgrade buttons throughout UI
- Stripe integration for payment
- Instant tier upgrade upon payment confirmation

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-14  
**Author**: EdGuide Product Team  
**Platform**: EdGuide (gai-observe.online)
