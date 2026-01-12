# CoursePlayerApp - Feature Gating Specification

## Overview

Feature gating is the mechanism that controls access to features and content based on a user's subscription tier. This document defines the complete feature access matrix, implementation strategy, and enforcement mechanisms.

---

## Subscription Tiers

### Tier 1: Basic ($97)
**Target Audience**: Beginners, casual learners, budget-conscious students

**Value Proposition**: "Start your learning journey with foundational courses and streaming access"

### Tier 2: Intermediate ($247)
**Target Audience**: Serious learners, professionals seeking skill advancement

**Value Proposition**: "Unlock interactive labs, downloadable content, and AI assistance"

### Tier 3: Advanced ($497)
**Target Audience**: Power users, career-focused professionals, enterprise learners

**Value Proposition**: "Complete access to all courses, unlimited AI support, and premium certifications"

---

## Feature Access Matrix

### Course Access

| Tier | Number of Courses | Course IDs | Description |
|------|------------------|------------|-------------|
| **Basic** | 5 foundational | `ai-01`, `ai-02`, `ds-01`, `ds-02`, `ml-01` | Introductory courses only |
| **Intermediate** | 8 courses | Basic + `ai-03`, `ds-03`, `ml-02` | Foundational + intermediate topics |
| **Advanced** | 9 courses (ALL) | Intermediate + `ai-04` | Complete catalog including advanced AI |

**Course List**:
- `ai-01`: Introduction to Artificial Intelligence
- `ai-02`: Machine Learning Fundamentals
- `ai-03`: Natural Language Processing with Transformers
- `ai-04`: Advanced Deep Learning Architectures (Advanced only)
- `ds-01`: Data Science Essentials
- `ds-02`: Data Visualization with Python
- `ds-03`: Big Data Analytics (Intermediate+)
- `ml-01`: Supervised Learning
- `ml-02`: Unsupervised Learning & Clustering (Intermediate+)

### Video Access

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| **Streaming** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Quality** | 480p | 720p | 1080p |
| **Download** | ❌ No | ✅ Yes (720p) | ✅ Yes (1080p + 720p) |
| **Quality Selection** | ❌ | ❌ | ✅ |
| **Speed Control** | ✅ 0.5x-2x | ✅ 0.5x-2x | ✅ 0.5x-2x |
| **Captions** | ✅ English | ✅ English | ✅ Multi-language |
| **Resume Playback** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Picture-in-Picture** | ✅ Yes | ✅ Yes | ✅ Yes |

**UI Behavior**:
- **Basic**: Show "⬇️ Download" button as disabled with tooltip: "Download available in Intermediate tier ($247)"
- **Intermediate**: Enable download button, single quality (720p)
- **Advanced**: Enable download with dropdown to select quality (1080p/720p)

### Slides Access

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| **View Slides** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Navigate** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Search** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Export PDF** | ❌ No | ✅ Yes | ✅ Yes |
| **Export PPTX** | ❌ No | ❌ No | ✅ Yes |
| **Annotations** | ❌ No | ❌ No | ✅ Yes |
| **Thumbnail View** | ✅ Yes | ✅ Yes | ✅ Yes |

**UI Behavior**:
- **Basic**: Show "Export" button as disabled with tooltip: "Export available in Intermediate tier ($247)"
- **Intermediate**: Enable "Export PDF" button
- **Advanced**: Enable "Export" dropdown with options: "PDF" and "PPTX"

### Lab Access

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| **View Lab Description** | ✅ Yes | ✅ Yes | ✅ Yes |
| **View Sample Code** | ✅ Read-only | ✅ Yes | ✅ Yes |
| **Execute Code** | ❌ No | ✅ Yes | ✅ Yes |
| **Save Progress** | ❌ No | ✅ Yes | ✅ Yes |
| **Lab Hints** | ❌ No | ✅ Yes | ✅ Yes |
| **Lab Solutions** | ❌ No | ✅ After completion | ✅ On-demand |
| **Access to SimulationPlayer** | ❌ No | ✅ Yes | ✅ Yes |

**UI Behavior**:
- **Basic**: Show "Start Lab" button as disabled with message: "Interactive labs available in Intermediate tier ($247). You can view the code below:"
  - Display lab code in read-only code viewer
- **Intermediate/Advanced**: Enable "Start Lab" button, launches SimulationPlayer in new tab

### AI Tutor Access

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| **AI Tutor Enabled** | ❌ No | ✅ Yes | ✅ Yes |
| **Monthly Quota** | 0 | 50 questions | Unlimited |
| **Context Awareness** | N/A | ✅ Course context | ✅ Course + history |
| **Response Time** | N/A | Standard | Priority (faster model) |
| **Hint Mode** | N/A | ✅ Yes | ✅ Yes |
| **Explain Mode** | N/A | ✅ Yes | ✅ Yes |
| **Code Examples** | N/A | ✅ Yes | ✅ Yes |

**UI Behavior**:
- **Basic**: Show AI Tutor icon with 🔒 lock symbol
  - On click: "AI Tutor is available starting from Intermediate tier ($247). Upgrade to get 50 AI-assisted questions per month!"
- **Intermediate**: Show AI Tutor chat interface
  - Display quota usage: "🤖 AI Tutor (45/50 questions used this month)"
  - When quota exceeded: "You've used all 50 questions this month. Resets on [date]. Upgrade to Advanced for unlimited questions!"
- **Advanced**: Show AI Tutor chat interface
  - Display: "🤖 AI Tutor (Unlimited)"

### Progress Tracking

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| **Videos Watched** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Slides Viewed** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Labs Completed** | ❌ N/A | ✅ Yes | ✅ Yes |
| **Quiz Scores** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Time Spent** | ❌ No | ✅ Yes | ✅ Yes |
| **Completion %** | ✅ Basic | ✅ Detailed | ✅ Detailed |
| **Heatmap View** | ❌ No | ❌ No | ✅ Yes |
| **Analytics Dashboard** | ❌ No | ✅ Basic | ✅ Advanced |
| **Export Progress** | ❌ No | ✅ CSV | ✅ CSV + JSON |

**Visualization Differences**:
- **Basic**: Simple progress bars
- **Intermediate**: Progress bars + time spent line chart + quiz performance
- **Advanced**: All of Intermediate + completion heatmap + predictive analytics

### Certificate Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| **Earn Certificates** | ✅ If qualified | ✅ If qualified | ✅ If qualified |
| **Certificate Design** | Basic template | Standard template | Premium template |
| **Download PDF** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Blockchain Verification** | ❌ No | ❌ No | ✅ Yes |
| **LinkedIn Share** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Custom Branding** | ❌ No | ❌ No | ✅ Yes (logo) |
| **Verification Link** | ✅ Basic | ✅ Standard | ✅ Enhanced |

**Certificate Templates**:
- **Basic**: Simple design, standard fonts, no special elements
- **Intermediate**: Professional design, company logo, signature
- **Advanced**: Premium design, blockchain badge, QR code for verification, custom branding option

### Support & Community

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| **Email Support** | ✅ Best effort | ✅ 48-hour response | ✅ 24-hour response |
| **Priority Support** | ❌ No | ❌ No | ✅ Yes |
| **Community Forums** | ✅ Yes | ✅ Yes | ✅ Yes |
| **1-on-1 Mentorship** | ❌ No | ❌ No | ✅ 2 sessions/year |
| **Office Hours** | ❌ No | ✅ Monthly | ✅ Weekly |

---

## Feature Flags Configuration

### Configuration File: `config/feature_flags.json`

```json
{
  "basic": {
    "video_download": false,
    "video_quality": "480p",
    "video_quality_options": ["480p"],
    "video_captions": ["en"],
    "slides_export": false,
    "slides_formats": [],
    "slides_annotations": false,
    "labs_interactive": false,
    "labs_view_code": true,
    "labs_hints": false,
    "labs_solutions": false,
    "ai_tutor_enabled": false,
    "ai_tutor_quota": 0,
    "ai_tutor_context": "none",
    "course_access": ["ai-01", "ai-02", "ds-01", "ds-02", "ml-01"],
    "progress_time_tracking": false,
    "progress_heatmap": false,
    "progress_export": false,
    "certificate_type": "basic",
    "certificate_blockchain": false,
    "support_priority": false,
    "support_sla_hours": null
  },
  "intermediate": {
    "video_download": true,
    "video_quality": "720p",
    "video_quality_options": ["720p"],
    "video_captions": ["en"],
    "slides_export": true,
    "slides_formats": ["pdf"],
    "slides_annotations": false,
    "labs_interactive": true,
    "labs_view_code": true,
    "labs_hints": true,
    "labs_solutions": "after_completion",
    "ai_tutor_enabled": true,
    "ai_tutor_quota": 50,
    "ai_tutor_context": "course",
    "course_access": ["ai-01", "ai-02", "ai-03", "ds-01", "ds-02", "ds-03", "ml-01", "ml-02"],
    "progress_time_tracking": true,
    "progress_heatmap": false,
    "progress_export": "csv",
    "certificate_type": "standard",
    "certificate_blockchain": false,
    "support_priority": false,
    "support_sla_hours": 48
  },
  "advanced": {
    "video_download": true,
    "video_quality": "1080p",
    "video_quality_options": ["1080p", "720p", "480p"],
    "video_captions": ["en", "es", "fr", "de", "zh"],
    "slides_export": true,
    "slides_formats": ["pdf", "pptx"],
    "slides_annotations": true,
    "labs_interactive": true,
    "labs_view_code": true,
    "labs_hints": true,
    "labs_solutions": "on_demand",
    "ai_tutor_enabled": true,
    "ai_tutor_quota": -1,
    "ai_tutor_context": "course_and_history",
    "course_access": "all",
    "progress_time_tracking": true,
    "progress_heatmap": true,
    "progress_export": "csv_and_json",
    "certificate_type": "premium",
    "certificate_blockchain": true,
    "support_priority": true,
    "support_sla_hours": 24,
    "mentorship_sessions": 2
  }
}
```

---

## Feature Gating Implementation

### 1. Feature Flag Loader

```python
# utils/feature_flags.py
import json
from typing import Dict, Any
from pathlib import Path

class FeatureFlags:
    _instance = None
    _flags = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_flags()
        return cls._instance
    
    @classmethod
    def _load_flags(cls):
        """Load feature flags from JSON config"""
        config_path = Path(__file__).parent.parent / "config" / "feature_flags.json"
        with open(config_path, 'r') as f:
            cls._flags = json.load(f)
    
    @classmethod
    def get_flags(cls, tier: str) -> Dict[str, Any]:
        """Get feature flags for a specific tier"""
        if cls._flags is None:
            cls._load_flags()
        
        tier_lower = tier.lower()
        if tier_lower not in cls._flags:
            raise ValueError(f"Invalid tier: {tier}. Must be 'basic', 'intermediate', or 'advanced'")
        
        return cls._flags[tier_lower]
    
    @classmethod
    def check_feature(cls, tier: str, feature: str) -> bool:
        """Check if a feature is enabled for a tier"""
        flags = cls.get_flags(tier)
        return flags.get(feature, False)
    
    @classmethod
    def get_course_access(cls, tier: str) -> list:
        """Get list of accessible course IDs for a tier"""
        flags = cls.get_flags(tier)
        access = flags.get("course_access", [])
        
        if access == "all":
            # Return all course IDs
            return ["ai-01", "ai-02", "ai-03", "ai-04", "ds-01", "ds-02", "ds-03", "ml-01", "ml-02"]
        
        return access
```

### 2. Feature Gate Decorator

```python
# utils/decorators.py
import streamlit as st
from functools import wraps
from typing import Callable, Optional

def require_tier(min_tier: str, upgrade_message: Optional[str] = None):
    """
    Decorator to enforce minimum tier requirement for a feature
    
    Args:
        min_tier: Minimum tier required ('intermediate' or 'advanced')
        upgrade_message: Custom message to show when access is denied
    """
    TIER_HIERARCHY = {"basic": 1, "intermediate": 2, "advanced": 3}
    
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get user's tier from session
            user_tier = st.session_state.get("tier", "basic").lower()
            
            # Check tier level
            if TIER_HIERARCHY.get(user_tier, 0) < TIER_HIERARCHY.get(min_tier, 999):
                # Access denied
                message = upgrade_message or f"This feature requires {min_tier.title()} tier or higher."
                st.warning(f"🔒 {message}")
                
                # Show upgrade CTA
                tier_prices = {"intermediate": "$247", "advanced": "$497"}
                st.info(f"💡 Upgrade to {min_tier.title()} tier ({tier_prices.get(min_tier, '')}) to unlock this feature!")
                
                return None
            
            # Access granted
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# Usage example:
@require_tier("intermediate", "Video downloads are available starting from Intermediate tier")
def download_video(video_id: str, quality: str):
    # This code only runs if user has intermediate or advanced tier
    return generate_download_url(video_id, quality)
```

### 3. UI Component Gating

```python
# utils/ui_components.py
import streamlit as st
from utils.feature_flags import FeatureFlags

def gated_button(
    label: str,
    feature_flag: str,
    tier: str,
    on_click: Callable = None,
    upgrade_tier: str = "intermediate"
):
    """
    Render a button that may be disabled based on feature flags
    
    Args:
        label: Button label
        feature_flag: Feature flag key to check
        tier: User's current tier
        on_click: Function to call when button is clicked (if enabled)
        upgrade_tier: Tier required to unlock this feature
    """
    flags = FeatureFlags.get_flags(tier)
    is_enabled = flags.get(feature_flag, False)
    
    if is_enabled:
        # Feature enabled - show active button
        if st.button(label):
            if on_click:
                on_click()
    else:
        # Feature disabled - show locked button with tooltip
        st.button(label, disabled=True, help=f"🔒 Unlock with {upgrade_tier.title()} tier")
        tier_prices = {"intermediate": "$247", "advanced": "$497"}
        st.caption(f"💡 Available in {upgrade_tier.title()} tier ({tier_prices.get(upgrade_tier, '')})")


def gated_download_button(
    label: str,
    data: bytes,
    file_name: str,
    tier: str,
    mime: str = "application/octet-stream"
):
    """Render a download button gated by tier"""
    flags = FeatureFlags.get_flags(tier)
    
    if flags.get("video_download") or flags.get("slides_export"):
        # Enabled - show download button
        st.download_button(
            label=label,
            data=data,
            file_name=file_name,
            mime=mime
        )
    else:
        # Disabled - show locked state
        st.button(label, disabled=True, help="🔒 Download available in Intermediate tier")
        st.caption("💡 Upgrade to Intermediate tier ($247) to download content")


def show_ai_tutor_quota(tier: str, user_id: str):
    """Display AI Tutor quota status"""
    flags = FeatureFlags.get_flags(tier)
    
    if not flags.get("ai_tutor_enabled"):
        st.sidebar.markdown("### 🤖 AI Tutor 🔒")
        st.sidebar.info("AI Tutor is available starting from **Intermediate tier ($247)**")
        return
    
    quota = flags.get("ai_tutor_quota")
    
    if quota == -1:
        # Unlimited
        st.sidebar.markdown("### 🤖 AI Tutor (Unlimited)")
        st.sidebar.success("Ask me anything! No limits.")
    else:
        # Limited quota
        from utils.quota_tracker import get_monthly_usage
        usage = get_monthly_usage(user_id)
        remaining = max(0, quota - usage)
        
        st.sidebar.markdown(f"### 🤖 AI Tutor ({usage}/{quota})")
        st.sidebar.progress(usage / quota)
        
        if remaining > 0:
            st.sidebar.caption(f"{remaining} questions remaining this month")
        else:
            st.sidebar.warning("Monthly quota reached!")
            st.sidebar.info("Upgrade to **Advanced tier ($497)** for unlimited AI assistance")
```

### 4. Course Access Control

```python
# utils/course_access.py
import streamlit as st
from utils.feature_flags import FeatureFlags

def check_course_access(course_id: str, tier: str) -> bool:
    """Check if user can access a specific course"""
    accessible_courses = FeatureFlags.get_course_access(tier)
    return course_id in accessible_courses


def filter_accessible_courses(all_courses: list, tier: str) -> tuple:
    """
    Filter courses by accessibility and return (accessible, locked)
    
    Returns:
        tuple: (list of accessible courses, list of locked courses)
    """
    accessible_courses = FeatureFlags.get_course_access(tier)
    
    accessible = [c for c in all_courses if c['id'] in accessible_courses]
    locked = [c for c in all_courses if c['id'] not in accessible_courses]
    
    return accessible, locked


def render_course_grid(courses: list, tier: str):
    """Render course grid with locked state for inaccessible courses"""
    accessible, locked = filter_accessible_courses(courses, tier)
    
    # Render accessible courses
    st.subheader("📚 Your Courses")
    cols = st.columns(3)
    for i, course in enumerate(accessible):
        with cols[i % 3]:
            render_course_card(course, accessible=True)
    
    # Render locked courses (preview)
    if locked:
        st.subheader("🔒 Unlock More Courses")
        cols = st.columns(3)
        for i, course in enumerate(locked):
            with cols[i % 3]:
                render_course_card(course, accessible=False)


def render_course_card(course: dict, accessible: bool):
    """Render a single course card"""
    if accessible:
        # Full color, clickable
        st.image(course['thumbnail'], use_column_width=True)
        st.markdown(f"**{course['title']}**")
        st.progress(course.get('progress', 0) / 100)
        if st.button("Continue", key=f"course_{course['id']}"):
            st.session_state['current_course'] = course['id']
            st.switch_page("pages/3_🎓_Course_Player.py")
    else:
        # Grayscale, locked overlay
        st.image(course['thumbnail'], use_column_width=True, output_format="PNG")
        st.markdown(f"**{course['title']}** 🔒")
        st.caption(f"Requires {course.get('required_tier', 'Intermediate')} tier")
        st.button("Upgrade to Unlock", key=f"locked_{course['id']}", disabled=True)
```

---

## Upgrade Flow

### Upgrade Prompt Strategy

**When to Show Upgrade Prompts**:
1. User clicks on a locked feature (e.g., download button, AI Tutor)
2. User tries to access a locked course
3. User exhausts their AI Tutor quota (Intermediate tier)
4. User views locked labs

**Prompt Types**:

1. **Inline Prompt** (within the feature UI):
   ```python
   st.info("💡 This feature is available in Intermediate tier ($247). [Upgrade Now](#)")
   ```

2. **Modal Prompt** (for significant upsell opportunities):
   ```python
   @st.dialog("Unlock Advanced Features")
   def show_upgrade_modal(from_tier: str, to_tier: str):
       st.markdown(f"### Upgrade from {from_tier.title()} to {to_tier.title()}")
       
       # Feature comparison
       st.markdown("""
       **You'll unlock:**
       - ✅ 3 additional courses
       - ✅ Video downloads (720p)
       - ✅ PDF slide exports
       - ✅ Interactive labs
       - ✅ AI Tutor (50 questions/month)
       """)
       
       st.markdown("**Price**: $247 (one-time payment)")
       
       if st.button("Upgrade Now"):
           # Redirect to upgrade page
           st.markdown("[Click here to upgrade](https://payment.gai-observe.com/upgrade)")
   ```

3. **Banner Prompt** (persistent reminder):
   ```python
   if tier == "basic":
       st.banner("💎 Upgrade to Intermediate tier to unlock downloads, labs, and AI Tutor! Only $247")
   ```

---

## A/B Testing Feature Flags

For experimentation and gradual rollout, we can add dynamic feature flags:

```json
{
  "experiments": {
    "ai_tutor_intermediate_100_questions": {
      "enabled": true,
      "rollout_percentage": 50,
      "description": "Test increasing AI Tutor quota for Intermediate tier to 100 questions"
    },
    "video_quality_720p_basic": {
      "enabled": false,
      "rollout_percentage": 0,
      "description": "Test offering 720p streaming for Basic tier"
    }
  }
}
```

---

## Enforcement Checklist

To prevent tier leakage (users accessing features they shouldn't have access to), enforce the following:

- [ ] **Server-side validation**: Never trust client-side tier checks alone
- [ ] **API-level gating**: CoursesGTM API validates tier before serving content
- [ ] **Double-check on actions**: Validate tier when user clicks download, launches lab, asks AI question
- [ ] **Audit logging**: Log all access attempts (successful and denied) for security analysis
- [ ] **Rate limiting**: Prevent brute-force attempts to bypass tier checks
- [ ] **Token refresh**: Re-validate tier on token refresh (every 24 hours)

---

## Testing Strategy

### Unit Tests

```python
# tests/test_feature_flags.py
import pytest
from utils.feature_flags import FeatureFlags

def test_basic_tier_video_download():
    flags = FeatureFlags.get_flags("basic")
    assert flags["video_download"] == False
    assert flags["video_quality"] == "480p"

def test_intermediate_tier_ai_tutor():
    flags = FeatureFlags.get_flags("intermediate")
    assert flags["ai_tutor_enabled"] == True
    assert flags["ai_tutor_quota"] == 50

def test_advanced_tier_unlimited_ai():
    flags = FeatureFlags.get_flags("advanced")
    assert flags["ai_tutor_quota"] == -1  # unlimited

def test_course_access_basic():
    courses = FeatureFlags.get_course_access("basic")
    assert len(courses) == 5
    assert "ai-04" not in courses  # advanced course

def test_course_access_advanced():
    courses = FeatureFlags.get_course_access("advanced")
    assert len(courses) == 9
    assert "ai-04" in courses
```

### Integration Tests

```python
# tests/test_feature_gating_integration.py
import pytest
from unittest.mock import Mock, patch
import streamlit as st

def test_locked_video_download_basic_tier():
    # Mock session with basic tier
    with patch.object(st, 'session_state', {"tier": "basic"}):
        result = attempt_video_download("video-123", "720p")
        assert result is None  # Download blocked
        # Verify upgrade message was shown

def test_ai_tutor_quota_enforcement():
    with patch('utils.quota_tracker.get_monthly_usage', return_value=50):
        with patch.object(st, 'session_state', {"tier": "intermediate", "user_id": "user123"}):
            result = ask_ai_tutor("What is NLP?")
            assert "quota reached" in result.lower()

def test_course_access_denied():
    with patch.object(st, 'session_state', {"tier": "basic"}):
        can_access = check_course_access("ai-04", "basic")
        assert can_access == False
```

---

## Edge Cases

### 1. Tier Downgrade
If a user downgrades (e.g., from Advanced to Intermediate):
- Existing downloaded videos remain accessible locally
- AI Tutor quota resets to 50/month
- Access to `ai-04` revoked (show "Re-upgrade to access" message)
- Progress in locked courses is preserved but view-only

### 2. Quota Reset
AI Tutor quota resets on the 1st of each month at 00:00 UTC

### 3. Mid-Month Upgrade
If user upgrades from Intermediate to Advanced mid-month:
- AI Tutor quota immediately becomes unlimited (no pro-rating)
- All locked courses become accessible instantly
- Video quality upgrades to 1080p for new streams

### 4. Expired License
If license expires:
- User is logged out on next session
- All in-progress downloads are interrupted
- Local cached content remains until cache clear

---

## Conclusion

This feature gating specification ensures:
- **Clear value proposition** for each tier
- **Secure enforcement** of access controls
- **Graceful degradation** and upgrade prompts
- **Testability** of feature gates
- **Flexibility** for future changes via JSON config

The system is designed to maximize conversions (Basic → Intermediate → Advanced) while providing excellent value at each tier.
