# Feature Gating Specification

## Platform Information
- **Platform**: EdGuide
- **Domain**: gai-observe.online
- **Purpose**: Define tier-based feature access and implementation strategy

---

## Overview

The feature gating system controls access to CoursePlayerApp functionality based on user license tiers. This creates a value ladder that encourages upgrades while ensuring fair access across all tiers.

### Tier Pricing
- **Basic**: $97 - Foundation learning experience
- **Intermediate**: $247 - Professional development tools
- **Advanced**: $497 - Elite learning environment

---

## Feature Access Matrix

### Complete Feature Comparison

| Feature Category | Feature | Basic ($97) | Intermediate ($247) | Advanced ($497) |
|-----------------|---------|-------------|---------------------|-----------------|
| **Video Access** | Stream videos (all resolutions) | ✅ | ✅ | ✅ |
| | Download videos (360p) | ❌ | ❌ | ❌ |
| | Download videos (720p) | ❌ | ✅ | ✅ |
| | Download videos (1080p) | ❌ | ❌ | ✅ |
| | Playback speed control | ✅ | ✅ | ✅ |
| | Chapter markers | ✅ | ✅ | ✅ |
| | Subtitles/captions | ✅ | ✅ | ✅ |
| | Picture-in-picture | ✅ | ✅ | ✅ |
| | Bookmark/resume | ✅ | ✅ | ✅ |
| **Slides** | View slides (online) | ✅ | ✅ | ✅ |
| | Export slides (PDF) | ❌ | ✅ | ✅ |
| | Export slides (PPTX) | ❌ | ❌ | ✅ |
| | Print slides | ❌ | ✅ | ✅ |
| **Labs** | View lab code | ✅ | ✅ | ✅ |
| | Execute labs (Jupyter) | ❌ | ✅ | ✅ |
| | Interactive code editor | ❌ | ✅ | ✅ |
| | Terminal access | ❌ | ✅ | ✅ |
| | Save lab progress | ❌ | ✅ | ✅ |
| | File upload/download | ❌ | ✅ | ✅ |
| | Package installation | ❌ | ✅ (limited) | ✅ (full) |
| **AI Tutor** | Access AI Tutor | ❌ | ✅ | ✅ |
| | Questions per month | 0 | 50 | Unlimited |
| | Context-aware answers | ❌ | ✅ | ✅ |
| | Code debugging | ❌ | ✅ | ✅ |
| | Practice problem generation | ❌ | ✅ | ✅ |
| | Priority response | ❌ | ❌ | ✅ |
| **Simulations** | Basic simulations | ❌ | ✅ | ✅ |
| | Advanced simulations | ❌ | ✅ (limited) | ✅ (unlimited) |
| | Simulation replays | ❌ | ✅ | ✅ |
| **Progress Tracking** | Basic progress tracking | ✅ | ✅ | ✅ |
| | Detailed analytics | ❌ | ✅ | ✅ |
| | Learning insights | ❌ | ❌ | ✅ |
| | Personalized recommendations | ❌ | ❌ | ✅ |
| | Progress export | ❌ | ✅ | ✅ |
| **Certificates** | Course completion certificate | ✅ | ✅ | ✅ |
| | Certificate template | Standard | Professional | Premium |
| | LinkedIn integration | ❌ | ✅ | ✅ |
| | Blockchain verification | ❌ | ❌ | ✅ |
| | Digital wallet support | ❌ | ❌ | ✅ |
| **Support** | Email support | ✅ | ✅ | ✅ |
| | Response time | 48 hours | 24 hours | 12 hours |
| | Priority support | ❌ | ❌ | ✅ |
| | Chat support | ❌ | ❌ | ✅ |
| **Community** | Access to community | ❌ | ❌ | ✅ |
| | Discord/Slack access | ❌ | ❌ | ✅ |
| | Early course access | ❌ | ❌ | ✅ |
| | Exclusive webinars | ❌ | ❌ | ✅ |

---

## Tier-Specific Details

### 🥉 Basic Tier ($97) - Foundation

**Philosophy**: Provide complete learning content access with consumption-focused features

#### Available Features ✅

1. **Video Streaming**
   - Stream all course videos (360p, 720p, 1080p)
   - Adaptive bitrate streaming
   - Playback speed control (0.5x - 2x)
   - Subtitles and captions
   - Chapter markers for navigation
   - Bookmark and resume functionality
   - Picture-in-picture mode
   - **Limitation**: Cannot download videos

2. **Slides Access**
   - View all course slides online
   - Navigate through slide decks
   - Zoom and pan functionality
   - **Limitation**: Cannot export or print

3. **Labs Viewing**
   - View all lab code and instructions
   - Syntax-highlighted code display
   - Read lab explanations
   - **Limitation**: View-only, cannot execute code

4. **Progress Tracking**
   - Track videos watched
   - Monitor course completion percentage
   - View module progress
   - Basic completion dashboard
   - **Limitation**: No detailed analytics

5. **Certificates**
   - Standard certificate upon course completion
   - PDF download
   - QR code for verification
   - **Limitation**: Standard template only, no LinkedIn integration

#### Locked Features 🔒

- ❌ **Video Download**: Upgrade to Intermediate for 720p downloads
- ❌ **Slide Export**: Upgrade to Intermediate to export PDF slides
- ❌ **Lab Execution**: Upgrade to Intermediate to run interactive labs
- ❌ **AI Tutor**: Upgrade to Intermediate for AI-powered assistance (50 questions/month)
- ❌ **Advanced Simulations**: Upgrade to Intermediate for hands-on simulations
- ❌ **Detailed Analytics**: Upgrade to Intermediate for learning insights
- ❌ **Community Access**: Upgrade to Advanced for Discord/Slack community

#### UI/UX Treatment

```python
# Example: Video Download Button (Locked)
st.button(
    "🔒 Download Video",
    disabled=True,
    help="Upgrade to Intermediate to download videos up to 720p"
)
st.info("⬆️ Upgrade to Intermediate tier to unlock video downloads")
```

**Visual Indicators**:
- 🔒 icon on locked features
- Disabled buttons with tooltip explanations
- Upgrade CTA prominently displayed
- Hover shows "Upgrade to [Tier] to unlock"

---

### 🥈 Intermediate Tier ($247) - Professional

**Philosophy**: Enable active learning with execution, downloads, and AI assistance

#### Everything in Basic PLUS ➕

1. **Video Downloads**
   - Download videos up to 720p resolution
   - Offline viewing capability
   - MP4 format with watermarking
   - Download quota: 100 videos/month
   - **Limitation**: 1080p downloads locked (Advanced only)

2. **Slide Export**
   - Export slides as PDF
   - Print-ready format
   - Annotatable PDFs
   - Download all slides in course
   - **Limitation**: PPTX export locked (Advanced only)

3. **Lab Execution**
   - Full Jupyter notebook execution
   - Interactive code editor (Monaco)
   - Web-based terminal access
   - Save lab progress to workspace
   - File upload/download (up to 100MB)
   - Package installation (pip, conda - curated list)
   - Sandbox environment (2 CPU, 4GB RAM)
   - 2-hour session timeout

4. **AI Tutor Access**
   - 50 questions per month quota
   - Context-aware Q&A
   - Code explanation and debugging
   - Concept clarification
   - Practice problem generation
   - Study tips and strategies
   - **Quota Display**: "23/50 questions remaining this month"
   - **Limitation**: Limited to 50 questions, resets monthly

5. **Advanced Simulations**
   - Access to basic and intermediate simulations
   - Limited advanced simulations (5/month)
   - Simulation progress tracking
   - Replay functionality

6. **Detailed Analytics**
   - Detailed progress dashboard
   - Time spent per module
   - Completion trends
   - Learning pace metrics
   - Strengths/weaknesses identification

7. **Professional Certificate**
   - Professional certificate template
   - LinkedIn integration (one-click share)
   - Enhanced verification URL
   - PDF + PNG formats

#### Still Locked Features 🔒

- ❌ **1080p Video Downloads**: Upgrade to Advanced
- ❌ **PPTX Slide Export**: Upgrade to Advanced
- ❌ **Unlimited AI Tutor**: Upgrade to Advanced for unlimited questions
- ❌ **All Simulations**: Upgrade to Advanced for unlimited access
- ❌ **Blockchain Certificates**: Upgrade to Advanced
- ❌ **Priority Support**: Upgrade to Advanced
- ❌ **Community Access**: Upgrade to Advanced

#### UI/UX Treatment

```python
# Example: AI Tutor with Quota Display
remaining = get_ai_tutor_quota_remaining(user_id)
st.sidebar.metric(
    "AI Tutor Questions",
    f"{remaining}/50",
    delta=f"{50 - remaining} used"
)

if remaining > 0:
    st.text_area("Ask your question")
    st.button("Submit Question")
else:
    st.warning("🔒 Monthly quota exceeded")
    st.info("⬆️ Upgrade to Advanced for unlimited AI Tutor questions")
```

**Visual Indicators**:
- Quota meters for AI Tutor and simulations
- Download buttons enabled with quality selector
- "Professional" badge on profile
- Upgrade prompts for Advanced features

---

### 🥇 Advanced Tier ($497) - Elite

**Philosophy**: Premium learning experience with unlimited access and exclusive benefits

#### Everything in Intermediate PLUS ➕

1. **Full Video Download Access**
   - Download videos up to 1080p resolution
   - Highest quality offline viewing
   - No download quota limits
   - Advanced DRM protection
   - Forensic watermarking for security

2. **Full Slide Export**
   - Export slides as both PDF and PPTX
   - Editable PowerPoint format
   - Maintain formatting and animations
   - Batch export entire courses

3. **Unlimited AI Tutor**
   - Unlimited questions (no quota)
   - Priority response time
   - Enhanced context awareness
   - Advanced code analysis
   - Personalized learning recommendations
   - Multi-turn conversations
   - Image/diagram explanations

4. **Unlimited Simulations**
   - Access to all simulations
   - No usage limits
   - Exclusive advanced scenarios
   - Unlimited replays
   - Simulation export functionality

5. **Advanced Analytics & Insights**
   - AI-powered learning insights
   - Personalized improvement plans
   - Predictive completion estimates
   - Comparative analytics (anonymized)
   - Detailed time-tracking reports
   - Export analytics data

6. **Premium Certificate**
   - Premium certificate template (designer-crafted)
   - Blockchain verification (immutable record)
   - Digital wallet support (Apple Wallet, Google Pay)
   - Enhanced LinkedIn integration
   - Social sharing with dynamic preview
   - Certificate portfolio page

7. **Priority Support**
   - 12-hour response time guarantee
   - Live chat support (business hours)
   - Priority email queue
   - Dedicated support specialist

8. **Exclusive Community Access**
   - Private Discord/Slack channels
   - Direct access to instructors
   - Peer networking opportunities
   - Exclusive webinars and Q&A sessions
   - Early access to new courses
   - Beta testing opportunities

9. **Additional Perks**
   - Course completion rewards (bonus content)
   - Exclusive learning resources
   - Career guidance resources
   - Industry expert sessions
   - Annual review with learning advisor

#### UI/UX Treatment

```python
# Example: All features unlocked
st.success("🥇 Advanced Tier - All Features Unlocked!")

# AI Tutor - No quota
st.sidebar.metric(
    "AI Tutor Questions",
    "Unlimited ♾️",
    delta="Premium access"
)

# Premium badge everywhere
st.markdown("![Advanced Badge](badge-advanced.svg)")
```

**Visual Indicators**:
- 🥇 "Advanced" badge on all pages
- "Unlimited" indicators on quotas
- No locked features
- Premium UI theme option (exclusive)
- VIP status indicators

---

## Implementation Guide

### Backend: Feature Gate Engine

```python
# core/feature_gate.py

from enum import Enum
from typing import Dict, List

class Tier(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Feature(Enum):
    # Video features
    VIDEO_STREAMING = "video_streaming"
    VIDEO_DOWNLOAD = "video_download"
    VIDEO_DOWNLOAD_720P = "video_download_720p"
    VIDEO_DOWNLOAD_1080P = "video_download_1080p"
    
    # Slide features
    SLIDE_VIEW = "slide_view"
    SLIDE_EXPORT_PDF = "slide_export_pdf"
    SLIDE_EXPORT_PPTX = "slide_export_pptx"
    
    # Lab features
    LAB_VIEW = "lab_view"
    LAB_EXECUTION = "lab_execution"
    LAB_TERMINAL = "lab_terminal"
    LAB_FILE_UPLOAD = "lab_file_upload"
    
    # AI Tutor features
    AI_TUTOR = "ai_tutor"
    AI_TUTOR_UNLIMITED = "ai_tutor_unlimited"
    
    # Simulation features
    SIMULATION_BASIC = "simulation_basic"
    SIMULATION_ADVANCED = "simulation_advanced"
    SIMULATION_UNLIMITED = "simulation_unlimited"
    
    # Certificate features
    CERTIFICATE = "certificate"
    CERTIFICATE_LINKEDIN = "certificate_linkedin"
    CERTIFICATE_BLOCKCHAIN = "certificate_blockchain"
    
    # Analytics features
    ANALYTICS_BASIC = "analytics_basic"
    ANALYTICS_DETAILED = "analytics_detailed"
    ANALYTICS_INSIGHTS = "analytics_insights"
    
    # Support features
    SUPPORT_EMAIL = "support_email"
    SUPPORT_PRIORITY = "support_priority"
    SUPPORT_CHAT = "support_chat"
    
    # Community features
    COMMUNITY_ACCESS = "community_access"

class FeatureGate:
    """
    Feature gating system for tier-based access control
    """
    
    # Feature access matrix: feature -> allowed tiers
    FEATURE_MATRIX: Dict[Feature, List[Tier]] = {
        # Video features
        Feature.VIDEO_STREAMING: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.VIDEO_DOWNLOAD: [Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.VIDEO_DOWNLOAD_720P: [Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.VIDEO_DOWNLOAD_1080P: [Tier.ADVANCED],
        
        # Slide features
        Feature.SLIDE_VIEW: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.SLIDE_EXPORT_PDF: [Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.SLIDE_EXPORT_PPTX: [Tier.ADVANCED],
        
        # Lab features
        Feature.LAB_VIEW: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.LAB_EXECUTION: [Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.LAB_TERMINAL: [Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.LAB_FILE_UPLOAD: [Tier.INTERMEDIATE, Tier.ADVANCED],
        
        # AI Tutor features
        Feature.AI_TUTOR: [Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.AI_TUTOR_UNLIMITED: [Tier.ADVANCED],
        
        # Simulation features
        Feature.SIMULATION_BASIC: [Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.SIMULATION_ADVANCED: [Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.SIMULATION_UNLIMITED: [Tier.ADVANCED],
        
        # Certificate features
        Feature.CERTIFICATE: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.CERTIFICATE_LINKEDIN: [Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.CERTIFICATE_BLOCKCHAIN: [Tier.ADVANCED],
        
        # Analytics features
        Feature.ANALYTICS_BASIC: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.ANALYTICS_DETAILED: [Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.ANALYTICS_INSIGHTS: [Tier.ADVANCED],
        
        # Support features
        Feature.SUPPORT_EMAIL: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
        Feature.SUPPORT_PRIORITY: [Tier.ADVANCED],
        Feature.SUPPORT_CHAT: [Tier.ADVANCED],
        
        # Community features
        Feature.COMMUNITY_ACCESS: [Tier.ADVANCED],
    }
    
    @staticmethod
    def can_access_feature(user_tier: str, feature: str) -> bool:
        """
        Check if user's tier has access to a feature
        
        Args:
            user_tier: User's license tier ("basic", "intermediate", "advanced")
            feature: Feature name (from Feature enum or string)
        
        Returns:
            bool: True if user has access, False otherwise
        """
        try:
            # Convert string to enums
            tier_enum = Tier(user_tier.lower())
            
            # Handle both string and enum inputs for feature
            if isinstance(feature, str):
                feature_enum = Feature(feature.lower())
            else:
                feature_enum = feature
            
            # Check access
            allowed_tiers = FeatureGate.FEATURE_MATRIX.get(feature_enum, [])
            return tier_enum in allowed_tiers
            
        except (ValueError, KeyError):
            # Invalid tier or feature
            return False
    
    @staticmethod
    def get_upgrade_tier(current_tier: str, feature: str) -> str:
        """
        Get the tier needed to unlock a feature
        
        Args:
            current_tier: User's current tier
            feature: Feature to unlock
        
        Returns:
            str: Required tier name or empty string if already has access
        """
        if FeatureGate.can_access_feature(current_tier, feature):
            return ""
        
        try:
            feature_enum = Feature(feature.lower())
            allowed_tiers = FeatureGate.FEATURE_MATRIX.get(feature_enum, [])
            
            # Find minimum tier that has access
            tier_order = [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED]
            for tier in tier_order:
                if tier in allowed_tiers:
                    return tier.value.capitalize()
            
        except (ValueError, KeyError):
            pass
        
        return "Advanced"
    
    @staticmethod
    def get_upgrade_message(current_tier: str, feature: str) -> str:
        """
        Get user-friendly message for locked features
        
        Args:
            current_tier: User's current tier
            feature: Locked feature
        
        Returns:
            str: Upgrade message
        """
        required_tier = FeatureGate.get_upgrade_tier(current_tier, feature)
        
        if not required_tier:
            return ""
        
        return f"Upgrade to {required_tier} to unlock this feature"
    
    @staticmethod
    def get_tier_features(tier: str) -> List[str]:
        """
        Get all features available for a tier
        
        Args:
            tier: Tier name
        
        Returns:
            List of feature names
        """
        try:
            tier_enum = Tier(tier.lower())
            features = []
            
            for feature, allowed_tiers in FeatureGate.FEATURE_MATRIX.items():
                if tier_enum in allowed_tiers:
                    features.append(feature.value)
            
            return features
            
        except ValueError:
            return []

# Example usage:
if __name__ == "__main__":
    # Check access
    print(FeatureGate.can_access_feature("basic", "video_streaming"))  # True
    print(FeatureGate.can_access_feature("basic", "ai_tutor"))  # False
    
    # Get upgrade message
    print(FeatureGate.get_upgrade_message("basic", "ai_tutor"))
    # Output: "Upgrade to Intermediate to unlock this feature"
    
    # Get all features for a tier
    print(FeatureGate.get_tier_features("intermediate"))
```

### Frontend: UI Components

```python
# ui/components/gated_component.py

import streamlit as st
from core.feature_gate import FeatureGate, Feature

def render_locked_feature(
    feature: str,
    user_tier: str,
    title: str,
    description: str = None
):
    """
    Render a locked feature with upgrade prompt
    
    Args:
        feature: Feature name
        user_tier: User's current tier
        title: Feature title
        description: Optional feature description
    """
    upgrade_tier = FeatureGate.get_upgrade_tier(user_tier, feature)
    
    st.markdown(f"### 🔒 {title}")
    
    if description:
        st.write(description)
    
    st.warning(f"This feature is locked in your {user_tier.capitalize()} tier")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"⬆️ Upgrade to **{upgrade_tier}** to unlock {title}")
    with col2:
        st.button(
            f"Upgrade Now",
            key=f"upgrade_{feature}",
            type="primary"
        )

def render_gated_button(
    feature: str,
    user_tier: str,
    label: str,
    on_click=None,
    **button_kwargs
):
    """
    Render a button that's enabled/disabled based on feature access
    
    Args:
        feature: Feature name
        user_tier: User's current tier
        label: Button label
        on_click: Click handler
        **button_kwargs: Additional button arguments
    """
    has_access = FeatureGate.can_access_feature(user_tier, feature)
    
    if has_access:
        return st.button(label, on_click=on_click, **button_kwargs)
    else:
        upgrade_msg = FeatureGate.get_upgrade_message(user_tier, feature)
        st.button(
            f"🔒 {label}",
            disabled=True,
            help=upgrade_msg,
            **button_kwargs
        )
        return False

def render_gated_section(
    feature: str,
    user_tier: str,
    content_func,
    locked_message: str = None
):
    """
    Render a section that's visible/locked based on feature access
    
    Args:
        feature: Feature name
        user_tier: User's current tier
        content_func: Function to render content if unlocked
        locked_message: Custom message for locked state
    """
    has_access = FeatureGate.can_access_feature(user_tier, feature)
    
    if has_access:
        content_func()
    else:
        upgrade_tier = FeatureGate.get_upgrade_tier(user_tier, feature)
        
        with st.container():
            st.markdown("---")
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if locked_message:
                    st.warning(f"🔒 {locked_message}")
                else:
                    st.warning(f"🔒 This content is locked")
                
                st.info(f"Upgrade to **{upgrade_tier}** to unlock")
            
            with col2:
                st.button("⬆️ Upgrade", key=f"upgrade_{feature}_section")
            
            st.markdown("---")

def render_quota_meter(
    label: str,
    used: int,
    total: int,
    unlimited: bool = False
):
    """
    Render a quota meter for limited resources
    
    Args:
        label: Quota label
        used: Amount used
        total: Total quota
        unlimited: Whether quota is unlimited
    """
    if unlimited:
        st.metric(
            label,
            "Unlimited ♾️",
            delta="Premium access",
            delta_color="off"
        )
    else:
        remaining = total - used
        percentage = (used / total * 100) if total > 0 else 0
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.metric(
                label,
                f"{remaining}/{total} remaining",
                delta=f"{used} used"
            )
        
        with col2:
            # Color code based on usage
            if percentage >= 90:
                st.error("⚠️ Low")
            elif percentage >= 70:
                st.warning("⚡ Medium")
            else:
                st.success("✓ Good")
        
        # Progress bar
        st.progress(percentage / 100)
        
        if percentage >= 80:
            st.info("💡 Upgrade to Advanced for unlimited access")
```

### API Layer: Access Control

```python
# main.py (FastAPI)

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.feature_gate import FeatureGate, Feature

app = FastAPI(title="CoursePlayerApp API")
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Validate JWT and return user info"""
    # JWT validation logic here
    # Returns: {"user_id": "123", "tier": "intermediate", ...}
    pass

def require_feature(feature: Feature):
    """
    Dependency to enforce feature access
    
    Usage:
        @app.get("/api/videos/{video_id}/download")
        async def download_video(
            user = Depends(require_feature(Feature.VIDEO_DOWNLOAD))
        ):
            ...
    """
    async def feature_checker(user: dict = Depends(get_current_user)):
        if not FeatureGate.can_access_feature(user["tier"], feature.value):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Feature not available in your tier",
                    "feature": feature.value,
                    "current_tier": user["tier"],
                    "required_tier": FeatureGate.get_upgrade_tier(
                        user["tier"],
                        feature.value
                    ),
                    "upgrade_message": FeatureGate.get_upgrade_message(
                        user["tier"],
                        feature.value
                    )
                }
            )
        return user
    
    return feature_checker

# Example endpoints with feature gating

@app.post("/api/videos/{video_id}/download")
async def download_video(
    video_id: str,
    quality: str,
    user: dict = Depends(require_feature(Feature.VIDEO_DOWNLOAD))
):
    """Download video endpoint (Intermediate/Advanced only)"""
    
    # Additional quality check for 1080p
    if quality == "1080p":
        if not FeatureGate.can_access_feature(user["tier"], Feature.VIDEO_DOWNLOAD_1080P.value):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="1080p downloads require Advanced tier"
            )
    
    # Generate download URL
    return {"download_url": f"https://cdn.gai-observe.online/videos/{video_id}/{quality}"}

@app.post("/api/ai-tutor/ask")
async def ask_ai_tutor(
    question: str,
    context: dict,
    user: dict = Depends(require_feature(Feature.AI_TUTOR))
):
    """AI Tutor endpoint (Intermediate/Advanced only)"""
    
    # Check quota for Intermediate tier
    if user["tier"] == "intermediate":
        quota_used = await get_ai_tutor_quota_used(user["user_id"])
        if quota_used >= 50:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Monthly quota exceeded",
                    "quota_used": quota_used,
                    "quota_limit": 50,
                    "upgrade_message": "Upgrade to Advanced for unlimited AI Tutor access"
                }
            )
    
    # Process question
    answer = await ai_tutor_service.ask(question, context, user["tier"])
    
    # Increment quota usage
    if user["tier"] == "intermediate":
        await increment_ai_tutor_quota(user["user_id"])
    
    return {"answer": answer, "quota_remaining": await get_quota_remaining(user)}

@app.get("/api/user/features")
async def get_user_features(user: dict = Depends(get_current_user)):
    """Get all available features for current user"""
    
    features = FeatureGate.get_tier_features(user["tier"])
    
    return {
        "tier": user["tier"],
        "features": features,
        "locked_features": [
            f.value for f in Feature
            if not FeatureGate.can_access_feature(user["tier"], f.value)
        ]
    }
```

---

## Quota Management

### AI Tutor Quota System

```python
# core/quota_manager.py

from datetime import datetime, timedelta
from typing import Optional
import redis
from sqlalchemy.orm import Session

class QuotaManager:
    """Manage usage quotas for limited features"""
    
    def __init__(self, redis_client: redis.Redis, db: Session):
        self.redis = redis_client
        self.db = db
    
    async def get_ai_tutor_quota(self, user_id: str, tier: str) -> dict:
        """
        Get AI Tutor quota information
        
        Returns:
            {
                "total": 50 or "unlimited",
                "used": 23,
                "remaining": 27 or "unlimited",
                "reset_date": "2026-02-01"
            }
        """
        if tier == "advanced":
            return {
                "total": "unlimited",
                "used": 0,
                "remaining": "unlimited",
                "reset_date": None
            }
        
        # For intermediate tier
        key = f"quota:ai_tutor:{user_id}:{datetime.now().strftime('%Y-%m')}"
        used = int(self.redis.get(key) or 0)
        total = 50
        
        # Calculate reset date (first day of next month)
        today = datetime.now()
        if today.month == 12:
            reset_date = datetime(today.year + 1, 1, 1)
        else:
            reset_date = datetime(today.year, today.month + 1, 1)
        
        return {
            "total": total,
            "used": used,
            "remaining": max(0, total - used),
            "reset_date": reset_date.strftime("%Y-%m-%d")
        }
    
    async def use_ai_tutor_quota(self, user_id: str, tier: str) -> bool:
        """
        Use one AI Tutor quota
        
        Returns:
            bool: True if quota available, False if exceeded
        """
        if tier == "advanced":
            return True  # Unlimited
        
        quota_info = await self.get_ai_tutor_quota(user_id, tier)
        
        if quota_info["remaining"] <= 0:
            return False
        
        # Increment usage
        key = f"quota:ai_tutor:{user_id}:{datetime.now().strftime('%Y-%m')}"
        self.redis.incr(key)
        
        # Set expiration to end of next month
        self.redis.expire(key, timedelta(days=60))
        
        return True
```

---

## Testing Feature Gates

```python
# tests/test_feature_gate.py

import pytest
from core.feature_gate import FeatureGate, Feature, Tier

class TestFeatureGate:
    
    def test_basic_tier_video_streaming(self):
        """Basic tier can stream videos"""
        assert FeatureGate.can_access_feature("basic", Feature.VIDEO_STREAMING.value)
    
    def test_basic_tier_cannot_download(self):
        """Basic tier cannot download videos"""
        assert not FeatureGate.can_access_feature("basic", Feature.VIDEO_DOWNLOAD.value)
    
    def test_intermediate_tier_ai_tutor(self):
        """Intermediate tier has AI Tutor access"""
        assert FeatureGate.can_access_feature("intermediate", Feature.AI_TUTOR.value)
    
    def test_intermediate_tier_limited_ai(self):
        """Intermediate tier does not have unlimited AI"""
        assert not FeatureGate.can_access_feature("intermediate", Feature.AI_TUTOR_UNLIMITED.value)
    
    def test_advanced_tier_all_features(self):
        """Advanced tier has access to all features"""
        for feature in Feature:
            assert FeatureGate.can_access_feature("advanced", feature.value)
    
    def test_upgrade_message_basic_to_intermediate(self):
        """Correct upgrade message for Basic -> Intermediate"""
        msg = FeatureGate.get_upgrade_message("basic", Feature.AI_TUTOR.value)
        assert "Intermediate" in msg
    
    def test_upgrade_message_intermediate_to_advanced(self):
        """Correct upgrade message for Intermediate -> Advanced"""
        msg = FeatureGate.get_upgrade_message("intermediate", Feature.AI_TUTOR_UNLIMITED.value)
        assert "Advanced" in msg
    
    def test_invalid_tier(self):
        """Invalid tier returns False"""
        assert not FeatureGate.can_access_feature("invalid", Feature.VIDEO_STREAMING.value)
    
    def test_invalid_feature(self):
        """Invalid feature returns False"""
        assert not FeatureGate.can_access_feature("basic", "invalid_feature")
```

---

## Marketing & Communication

### Tier Comparison for Marketing

Use this comparison in:
- Pricing page
- Upgrade prompts
- Email campaigns
- In-app messaging

**Key Value Props by Tier**:

| Tier | Primary Value Proposition | Best For |
|------|--------------------------|----------|
| **Basic** | "Master the concepts with complete course access" | Students who want to learn at their own pace with flexibility to upgrade later |
| **Intermediate** | "Become job-ready with hands-on practice and AI assistance" | Professionals seeking career advancement with practical skills |
| **Advanced** | "Elite learning experience with unlimited resources and exclusive community" | Serious learners who want the best tools and support for rapid mastery |

---

## Related Documentation

- [System Architecture](./ARCHITECTURE.md)
- [Video Player Specification](./VIDEO_PLAYER.md)
- [Lab Runner Specification](./LAB_RUNNER.md)
- [AI Tutor Specification](./AI_TUTOR.md)
- [UI/UX Design](./UI_UX_DESIGN.md)

---

**Last Updated**: January 2026  
**Platform**: EdGuide (gai-observe.online)  
**Version**: 1.0
