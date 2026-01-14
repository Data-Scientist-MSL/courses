# Feature Gating Specification

## Overview

Feature gating is the core mechanism that controls access to CoursePlayerApp functionality based on user subscription tier (Basic, Intermediate, Advanced). This specification defines the exact features available at each tier, implementation strategies, and enforcement mechanisms.

---

## Tier Pricing & Positioning

| Tier | Price | Target Audience | Value Proposition |
|------|-------|----------------|-------------------|
| **Basic** | $97 | Students exploring data science | Foundation courses, streaming-only, basic tracking |
| **Intermediate** | $247 | Learners committing to skill-building | Full interactivity, AI assistance, downloadable content |
| **Advanced** | $497 | Professionals seeking mastery | Premium experience, unlimited AI, blockchain certificates |

---

## Feature Access Matrix

### Basic Tier ($97)

#### ✅ **Allowed Features**

**Course Access**:
- Access to **5 foundational courses**:
  - `ai-01`: Introduction to AI
  - `ai-02`: Machine Learning Basics
  - `ds-01`: Data Science Fundamentals
  - `ds-02`: Data Visualization
  - `ml-01`: Supervised Learning

**Video Access**:
- **Stream Only** (no download)
- **Quality**: 480p
- Playback controls: Play, Pause, Seek
- Speed control: 0.5x, 1x, 1.25x, 1.5x, 2x
- Captions/subtitles available
- Resume from last position

**Slides Access**:
- **View Only** (no export)
- Navigation: Previous, Next, Jump to slide
- Thumbnail view
- Zoom controls
- No download or print capability

**Labs**:
- **Read-Only Preview**
- View lab instructions and objectives
- View code snippets (no execution)
- See expected output
- Cannot launch SimulationPlayer

**AI Tutor**:
- ❌ **Disabled** (0 questions)
- Show upgrade prompt: "AI Tutor available in Intermediate tier ($247)"

**Progress Tracking**:
- **Basic Dashboard**
- Course completion percentage
- Videos watched count
- Simple progress bars
- No detailed analytics

**Certificates**:
- ✅ **View Earned Certificates** (if course completed)
- Standard PDF download
- Basic design template
- No blockchain verification

**Support**:
- Community forum access
- FAQ documentation

#### ❌ **Restricted Features**
- No video download
- No slides export
- No interactive labs
- No AI Tutor
- No advanced analytics
- No blockchain certificates
- No priority support

---

### Intermediate Tier ($247)

#### ✅ **Allowed Features**

**Course Access**:
- Access to **8 courses** (foundational + intermediate):
  - All Basic tier courses (ai-01, ai-02, ds-01, ds-02, ml-01)
  - **Plus**: `ai-03`: Natural Language Processing
  - **Plus**: `ds-03`: Statistical Modeling
  - **Plus**: `ml-02`: Unsupervised Learning

**Video Access**:
- **Stream + Download**
- **Quality**: 720p
- All Basic tier features, plus:
  - Download button for offline viewing
  - Multiple quality options (480p, 720p)
  - Downloaded videos playable for 30 days

**Slides Access**:
- **View + Export**
- All Basic tier features, plus:
  - Export to **PDF**
  - Print capability
  - Download slide deck as single PDF

**Labs**:
- **Interactive Execution**
- Launch SimulationPlayer for hands-on coding
- Execute code in real-time
- See live output
- Submit solutions for grading
- Access to all lab environments

**AI Tutor**:
- ✅ **Enabled** with **50 questions/month quota**
- Context-aware responses
- Hints and explanations
- Resource suggestions
- Quota tracking displayed
- Monthly reset on subscription anniversary

**Progress Tracking**:
- **Advanced Dashboard**
- All Basic tier features, plus:
  - Time spent per course/module
  - Quiz scores and attempts
  - Lab completion status and scores
  - Video watch completion percentage
  - Weekly activity summary

**Certificates**:
- ✅ **Enhanced Design**
- Professional certificate template
- Course completion score displayed
- Shareable to LinkedIn
- PDF download
- No blockchain verification

**Support**:
- Email support (48-hour response time)
- Community forum access
- FAQ documentation

#### ❌ **Restricted Features**
- No 1080p video quality
- No PPTX export
- No unlimited AI Tutor
- No blockchain certificates
- No priority support
- No access to advanced AI courses

---

### Advanced Tier ($497)

#### ✅ **Allowed Features**

**Course Access**:
- Access to **ALL 9 courses** (complete catalog):
  - All Intermediate tier courses
  - **Plus**: `ai-04`: Deep Learning & Neural Networks
  - Full access to future course releases (within subscription period)

**Video Access**:
- **Stream + Download**
- **Quality**: 1080p (highest quality)
- All Intermediate tier features, plus:
  - Download in multiple formats (MP4, WebM)
  - Downloaded videos playable indefinitely
  - Priority streaming (faster CDN)

**Slides Access**:
- **View + Export (Multiple Formats)**
- All Intermediate tier features, plus:
  - Export to **PDF** and **PPTX**
  - Editable PowerPoint files
  - High-resolution image export
  - Batch download all slides

**Labs**:
- **Full Access + Priority Resources**
- All Intermediate tier features, plus:
  - Priority lab instances (faster startup)
  - Extended session time (no timeouts)
  - Access to advanced simulations
  - Code solution downloads

**AI Tutor**:
- ✅ **Unlimited Questions** (no quota)
- All Intermediate tier features, plus:
  - No monthly limit
  - Priority response generation
  - Advanced prompting capabilities
  - Conversation history saved

**Progress Tracking**:
- **Detailed Analytics + Insights**
- All Intermediate tier features, plus:
  - **Heatmap**: Calendar view of activity
  - **Time Series**: Learning trends over time
  - **Comparative Analytics**: Peer benchmarking (anonymous)
  - **Predictive Insights**: Completion estimates
  - Export analytics as CSV/Excel

**Certificates**:
- ✅ **Premium + Blockchain Verified**
- Premium certificate design
- **Blockchain verification** (Ethereum/Polygon)
- Unique certificate ID
- Public verification link
- Tamper-proof record
- LinkedIn integration
- PDF + digital wallet export

**Support**:
- **Priority Support**
- Email support (24-hour response time)
- Live chat during business hours
- 1-on-1 mentorship session (quarterly)
- Course content suggestions

#### ❌ **No Restrictions**
All features unlocked.

---

## Feature Flags Configuration

### Implementation: `feature_flags.json`

```json
{
  "basic": {
    "tier_name": "Basic",
    "tier_price": 97,
    "video_download": false,
    "video_quality": "480p",
    "video_quality_options": ["480p"],
    "slides_export": false,
    "slides_format": [],
    "labs_interactive": false,
    "labs_priority": false,
    "ai_tutor_enabled": false,
    "ai_tutor_quota": 0,
    "ai_tutor_priority": false,
    "course_access": ["ai-01", "ai-02", "ds-01", "ds-02", "ml-01"],
    "analytics_level": "basic",
    "analytics_heatmap": false,
    "analytics_export": false,
    "blockchain_certificates": false,
    "support_level": "community",
    "support_response_time": null
  },
  "intermediate": {
    "tier_name": "Intermediate",
    "tier_price": 247,
    "video_download": true,
    "video_quality": "720p",
    "video_quality_options": ["480p", "720p"],
    "video_download_expiry_days": 30,
    "slides_export": true,
    "slides_format": ["pdf"],
    "labs_interactive": true,
    "labs_priority": false,
    "ai_tutor_enabled": true,
    "ai_tutor_quota": 50,
    "ai_tutor_priority": false,
    "course_access": [
      "ai-01", "ai-02", "ai-03", 
      "ds-01", "ds-02", "ds-03", 
      "ml-01", "ml-02"
    ],
    "analytics_level": "advanced",
    "analytics_heatmap": false,
    "analytics_export": false,
    "blockchain_certificates": false,
    "support_level": "email",
    "support_response_time": 48
  },
  "advanced": {
    "tier_name": "Advanced",
    "tier_price": 497,
    "video_download": true,
    "video_quality": "1080p",
    "video_quality_options": ["480p", "720p", "1080p"],
    "video_download_expiry_days": -1,
    "video_formats": ["mp4", "webm"],
    "slides_export": true,
    "slides_format": ["pdf", "pptx"],
    "slides_high_res": true,
    "labs_interactive": true,
    "labs_priority": true,
    "labs_extended_sessions": true,
    "ai_tutor_enabled": true,
    "ai_tutor_quota": -1,
    "ai_tutor_priority": true,
    "ai_tutor_history": true,
    "course_access": "all",
    "analytics_level": "detailed",
    "analytics_heatmap": true,
    "analytics_export": true,
    "analytics_peer_benchmark": true,
    "blockchain_certificates": true,
    "certificate_blockchain": "polygon",
    "support_level": "priority",
    "support_response_time": 24,
    "support_live_chat": true,
    "mentorship_sessions": 4
  }
}
```

---

## Feature Gating Implementation

### 1. Loading Feature Flags

```python
# utils/feature_flags.py
import json
from typing import Dict, Any

def load_feature_flags() -> Dict[str, Any]:
    """Load feature flags from JSON configuration"""
    with open('config/feature_flags.json', 'r') as f:
        return json.load(f)

def get_tier_config(tier: str) -> Dict[str, Any]:
    """Get configuration for specific tier"""
    flags = load_feature_flags()
    tier_lower = tier.lower()
    
    if tier_lower not in flags:
        raise ValueError(f"Invalid tier: {tier}")
    
    return flags[tier_lower]
```

### 2. Feature Check Decorator

```python
# utils/decorators.py
import streamlit as st
from functools import wraps

def requires_feature(feature_key: str, fallback_message: str = None):
    """Decorator to gate features based on tier configuration"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tier = st.session_state.get('tier', 'basic').lower()
            config = get_tier_config(tier)
            
            if not config.get(feature_key, False):
                if fallback_message:
                    st.warning(fallback_message)
                else:
                    st.warning(f"🔒 This feature is not available in your {tier.title()} tier.")
                    show_upgrade_prompt(tier)
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### 3. Course Access Check

```python
# utils/access_control.py
import streamlit as st

def has_course_access(course_id: str) -> bool:
    """Check if user has access to specific course"""
    tier = st.session_state.get('tier', 'basic').lower()
    config = get_tier_config(tier)
    
    course_access = config['course_access']
    
    # Advanced tier has access to all courses
    if course_access == "all":
        return True
    
    # Check if course in allowed list
    return course_id in course_access

def filter_accessible_courses(all_courses: list) -> list:
    """Filter courses based on tier access"""
    return [
        course for course in all_courses 
        if has_course_access(course['course_id'])
    ]
```

### 4. Video Download Gating

```python
# components/video_player.py
import streamlit as st

@requires_feature('video_download', 
                  "📥 Video download available in Intermediate tier ($247)")
def render_download_button(video_url: str, video_title: str):
    """Render video download button (gated by tier)"""
    tier = st.session_state['tier'].lower()
    config = get_tier_config(tier)
    
    quality = config['video_quality']
    
    st.download_button(
        label=f"📥 Download Video ({quality})",
        data=get_video_file(video_url, quality),
        file_name=f"{video_title}_{quality}.mp4",
        mime="video/mp4"
    )
```

### 5. AI Tutor Quota Enforcement

```python
# components/ai_tutor.py
import streamlit as st
from utils.feature_flags import get_tier_config
from utils.database import get_ai_usage, increment_ai_usage

def check_ai_tutor_quota() -> tuple[bool, str]:
    """Check if user can ask AI Tutor question"""
    tier = st.session_state.get('tier', 'basic').lower()
    config = get_tier_config(tier)
    
    if not config['ai_tutor_enabled']:
        return False, "AI Tutor is available in Intermediate tier ($247). Upgrade to unlock!"
    
    quota = config['ai_tutor_quota']
    
    # Unlimited quota (-1)
    if quota == -1:
        return True, "Unlimited questions remaining"
    
    # Check usage
    user_id = st.session_state['user_id']
    usage = get_ai_usage(user_id)
    
    if usage >= quota:
        return False, f"You've used all {quota} questions this month. Upgrade to Advanced for unlimited!"
    
    remaining = quota - usage
    return True, f"{remaining}/{quota} questions remaining this month"

def ask_ai_tutor(question: str, context: dict) -> str:
    """Ask question to AI Tutor with quota check"""
    can_ask, message = check_ai_tutor_quota()
    
    if not can_ask:
        return message
    
    # Process question with OLLAMA
    response = ollama_chat(question, context)
    
    # Increment usage (unless unlimited)
    tier = st.session_state['tier'].lower()
    config = get_tier_config(tier)
    
    if config['ai_tutor_quota'] != -1:
        increment_ai_usage(st.session_state['user_id'])
    
    return response
```

### 6. Slides Export Gating

```python
# components/slides_viewer.py
import streamlit as st

def render_export_buttons(slides_data: dict):
    """Render slide export buttons based on tier"""
    tier = st.session_state.get('tier', 'basic').lower()
    config = get_tier_config(tier)
    
    if not config['slides_export']:
        st.info("🔒 Slide export available in Intermediate tier ($247)")
        return
    
    export_formats = config['slides_format']
    
    col1, col2 = st.columns(2)
    
    if 'pdf' in export_formats:
        with col1:
            if st.button("📄 Export as PDF"):
                pdf_data = generate_pdf(slides_data)
                st.download_button(
                    "Download PDF",
                    data=pdf_data,
                    file_name=f"{slides_data['title']}.pdf",
                    mime="application/pdf"
                )
    
    if 'pptx' in export_formats:
        with col2:
            if st.button("📊 Export as PPTX"):
                pptx_data = generate_pptx(slides_data)
                st.download_button(
                    "Download PPTX",
                    data=pptx_data,
                    file_name=f"{slides_data['title']}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
```

### 7. Lab Access Gating

```python
# components/lab_launcher.py
import streamlit as st

def render_lab_launcher(lab_data: dict):
    """Render lab launcher with tier-appropriate access"""
    tier = st.session_state.get('tier', 'basic').lower()
    config = get_tier_config(tier)
    
    st.subheader(lab_data['title'])
    st.write(lab_data['description'])
    
    if not config['labs_interactive']:
        # Basic tier: Read-only preview
        st.warning("🔒 Interactive labs available in Intermediate tier ($247)")
        
        with st.expander("View Lab Preview (Read-Only)"):
            st.code(lab_data['starter_code'], language='python')
            st.write("**Expected Output:**")
            st.code(lab_data['expected_output'])
        
        show_upgrade_prompt('basic')
    
    else:
        # Intermediate/Advanced: Interactive labs
        priority = config.get('labs_priority', False)
        
        if priority:
            st.success("⚡ Priority lab resources enabled")
        
        if st.button("🚀 Start Interactive Lab", type="primary"):
            launch_simulation_player(lab_data['lab_id'])
```

---

## Upgrade Prompts & Messaging

### Upgrade Prompt Component

```python
# components/upgrade_prompt.py
import streamlit as st

TIER_BENEFITS = {
    'basic': {
        'next_tier': 'Intermediate',
        'price': 247,
        'benefits': [
            "✅ 3 additional courses",
            "✅ Download videos (720p)",
            "✅ Export slides to PDF",
            "✅ Interactive coding labs",
            "✅ AI Tutor (50 Q/month)",
            "✅ Advanced progress tracking"
        ]
    },
    'intermediate': {
        'next_tier': 'Advanced',
        'price': 497,
        'benefits': [
            "✅ All 9 courses unlocked",
            "✅ Download videos (1080p)",
            "✅ Export slides to PDF & PPTX",
            "✅ Unlimited AI Tutor",
            "✅ Blockchain certificates",
            "✅ Priority support"
        ]
    }
}

def show_upgrade_prompt(current_tier: str):
    """Display upgrade prompt based on current tier"""
    if current_tier == 'advanced':
        return  # Already at highest tier
    
    info = TIER_BENEFITS[current_tier]
    
    st.info(f"**Upgrade to {info['next_tier']} - ${info['price']}**")
    
    with st.expander("See what you'll unlock"):
        for benefit in info['benefits']:
            st.write(benefit)
        
        if st.button(f"Upgrade to {info['next_tier']}", key=f"upgrade_{current_tier}"):
            st.switch_page("pages/7_⚙️_Settings.py")
```

---

## Testing Feature Gates

### Unit Tests

```python
# tests/test_feature_gating.py
import pytest
from utils.feature_flags import get_tier_config
from utils.access_control import has_course_access

def test_basic_tier_video_download():
    config = get_tier_config('basic')
    assert config['video_download'] == False
    assert config['video_quality'] == '480p'

def test_intermediate_tier_ai_tutor():
    config = get_tier_config('intermediate')
    assert config['ai_tutor_enabled'] == True
    assert config['ai_tutor_quota'] == 50

def test_advanced_tier_course_access():
    config = get_tier_config('advanced')
    assert config['course_access'] == 'all'
    assert config['ai_tutor_quota'] == -1  # unlimited

def test_course_access_basic():
    # Mock session state
    st.session_state['tier'] = 'basic'
    
    assert has_course_access('ai-01') == True
    assert has_course_access('ai-03') == False  # Intermediate course
    assert has_course_access('ai-04') == False  # Advanced course

def test_course_access_advanced():
    st.session_state['tier'] = 'advanced'
    
    # Advanced has access to all
    assert has_course_access('ai-01') == True
    assert has_course_access('ai-03') == True
    assert has_course_access('ai-04') == True
```

---

## Analytics & Monitoring

### Track Feature Usage by Tier

```python
# utils/analytics.py
def log_feature_usage(feature_name: str, tier: str):
    """Log feature usage for analytics"""
    # Track which features are used by which tiers
    # Helps identify:
    # - Popular features for each tier
    # - Conversion opportunities (Basic users hitting gates)
    # - Feature adoption rates
    
    analytics_event = {
        'event': 'feature_used',
        'feature': feature_name,
        'tier': tier,
        'timestamp': datetime.now(),
        'user_id': st.session_state.get('user_id')
    }
    
    # Send to analytics platform
    send_to_analytics(analytics_event)

def log_upgrade_prompt_shown(current_tier: str, feature_blocked: str):
    """Log when upgrade prompts are shown"""
    analytics_event = {
        'event': 'upgrade_prompt_shown',
        'current_tier': current_tier,
        'feature_blocked': feature_blocked,
        'timestamp': datetime.now(),
        'user_id': st.session_state.get('user_id')
    }
    
    send_to_analytics(analytics_event)
```

---

## Tier Migration

### Handling Tier Upgrades

```python
# utils/tier_migration.py
def handle_tier_upgrade(user_id: str, old_tier: str, new_tier: str):
    """Handle user tier upgrade"""
    # 1. Update session state
    st.session_state['tier'] = new_tier
    
    # 2. Refresh course access
    refresh_course_list()
    
    # 3. Reset AI Tutor quota if upgrading to Advanced
    if new_tier == 'advanced':
        reset_ai_quota(user_id)
    
    # 4. Grant access to previously locked features
    unlock_features(new_tier)
    
    # 5. Log upgrade event
    log_upgrade_event(user_id, old_tier, new_tier)
    
    # 6. Show success message
    st.success(f"🎉 Upgraded to {new_tier.title()} tier! Enjoy your new features.")
    st.balloons()
```

---

## Conclusion

This feature gating specification ensures clear tier differentiation, prevents unauthorized feature access, and provides smooth upgrade paths. Implementation must enforce gates server-side (never trust client) and provide clear, non-intrusive upgrade messaging.

