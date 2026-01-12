# Feature Gating System

## Overview

CoursePlayerApp implements a comprehensive tier-based feature gating system that controls access to features and content based on the user's subscription tier. This system ensures a clear value progression from Basic to Advanced tiers while maintaining a positive experience for all users.

---

## Subscription Tiers

### Basic Tier - $97/year
**Target Audience**: Casual learners, students exploring data science

**Core Value**: Access to fundamental courses with essential learning features

**Features**:

**✅ Course Access**:
- 5 fundamental courses available:
  - Data Scientist's Toolbox
  - R Programming
  - Getting and Cleaning Data
  - Exploratory Data Analysis
  - Reproducible Research
- All lessons and modules within these courses
- Course outlines and descriptions

**✅ Video Streaming**:
- Stream-only access (no download)
- Maximum quality: 720p
- Playback speed control (0.5x - 2x)
- Basic playback controls (play, pause, seek)
- Auto-generated closed captions
- Keyboard shortcuts

**✅ Slide Viewing**:
- View slides in browser
- Navigate through slides (prev/next)
- Zoom controls
- Search within slides
- ❌ No download capability
- ❌ No offline access

**✅ Lab Access - View-Only Mode**:
- Read-through of lab instructions
- View pre-completed code examples
- See expected outputs
- Read explanations
- ❌ Cannot edit or execute code
- ❌ Cannot create custom scenarios
- **Upgrade Prompt**: "Unlock interactive labs with Intermediate tier"

**❌ AI Tutor**:
- Not available for Basic tier users
- Placeholder shown with upgrade prompt
- **Message**: "Get instant answers to your questions! Upgrade to Intermediate for AI-powered tutoring (50 questions/month)"

**❌ Downloads**:
- No video downloads
- No slide downloads
- No code example downloads
- No dataset downloads
- **Upgrade Prompt**: "Download all materials for offline learning with Intermediate tier"

**❌ Certificates**:
- No certificate generation
- Cannot take certification exams
- **Message**: "Complete courses and earn verified certificates with Intermediate tier"

**Progress Tracking** (Available):
- Course completion percentage
- Lessons completed
- Time spent learning
- Basic achievements (e.g., "First lesson completed")

---

### Intermediate Tier - $247/year
**Target Audience**: Serious learners, career switchers, professionals upskilling

**Core Value**: Full interactive learning experience with AI assistance and credentials

**Features**:

**✅ Course Access**:
- All 5 Basic courses PLUS 3 additional courses:
  - Statistical Inference
  - Regression Models
  - Practical Machine Learning
- Total: 8 courses
- Priority access to new course releases

**✅ Video Streaming & Download**:
- Stream AND download capability
- Maximum quality: 1080p (Full HD)
- Offline viewing (downloads stored locally)
- Download limits: 50 GB/month
- DRM protection on downloaded content (expires with license)
- Background downloads (queue multiple videos)

**✅ Slide Downloads**:
- Download slides as PDF
- Print-friendly formatting
- Annotations preserved (if supported)
- Batch download (entire course at once)
- File size per course: ~50-100 MB

**✅ Interactive Labs**:
- Full interactive mode
- Edit and execute code in browser
- Jupyter notebook integration
- Save progress and checkpoints
- Terminal access (limited commands)
- 100 lab hours/month included
- **Upgrade for**: Custom scenarios (Advanced only)

**✅ AI Tutor - Limited**:
- 50 questions per month
- Resets on billing cycle (monthly)
- Context-aware responses
- Code assistance (explain, debug)
- Concept clarification
- Conversation history saved
- Quota tracking visible in UI
- **Quota Exceeded Message**: "You've used all 50 questions this month. Upgrade to Advanced for unlimited AI tutoring!"

**✅ Downloads - Code & Data**:
- Download code examples (Python, R scripts)
- Download datasets (CSV, JSON, etc.)
- Download supplementary materials
- Monthly limit: 5 GB

**✅ Certificates**:
- Digital certificates upon course completion
- PDF download
- LinkedIn sharing integration
- Verification URL (validates on our platform)
- Includes: Name, course title, completion date, unique ID
- ❌ Not blockchain-verified (Advanced only)

**✅ Progress Tracking** (Enhanced):
- All Basic features
- Lab completion tracking
- Quiz performance analytics
- Learning pace insights
- Advanced achievements (e.g., "Week streak", "Perfect quiz")

**✅ Community Access**:
- Discussion forums
- Peer Q&A
- Study groups

---

### Advanced Tier - $497/year
**Target Audience**: Professionals, career data scientists, certificate seekers

**Core Value**: Premium unlimited experience with maximum flexibility and verified credentials

**Features**:

**✅ Course Access**:
- All 9 courses (full catalog):
  - All 8 from Intermediate
  - Developing Data Products
- Early access to beta courses
- Lifetime access to course updates
- Exclusive advanced modules

**✅ Video Streaming & Download**:
- Unlimited downloads
- Maximum quality: 4K (2160p) where available
- No monthly limits
- Highest bitrate available
- Batch download entire courses
- Export to external devices

**✅ Slide Downloads - Full Access**:
- Download as PDF AND editable PowerPoint (.pptx)
- Includes speaker notes
- Editable for personal use
- Source files (Markdown, LaTeX where available)
- Unlimited downloads

**✅ Interactive Labs - Full Access**:
- Everything from Intermediate PLUS:
- Custom scenario creation
- Unlimited lab hours
- Advanced terminal access (full shell)
- GPU access (for ML workloads)
- Persistent lab environments (save state)
- Export lab work (Jupyter notebooks)
- Collaboration features (share labs)

**✅ AI Tutor - Unlimited**:
- Unlimited questions (no monthly quota)
- Priority response generation
- Advanced context window (8K tokens vs 4K)
- Multi-turn conversations (deeper discussions)
- Code generation assistance
- Project feedback
- Personalized learning recommendations
- All conversation history saved indefinitely

**✅ Downloads - Unlimited**:
- No limits on any content type
- Bulk download tools
- API access for programmatic downloads
- Offline course packages

**✅ Certificates - Premium**:
- Blockchain-verified certificates
- Stored on Ethereum/Polygon blockchain
- Immutable, tamper-proof verification
- Premium certificate design
- Wallet integration (MetaMask)
- NFT certificate option
- Employer verification API
- Includes all Intermediate certificate features

**✅ Priority Support**:
- Dedicated support channel
- < 4 hour response time (business hours)
- Video call support (scheduled)
- Direct access to instructors (office hours)
- Custom learning path consultation

**✅ Advanced Analytics**:
- Detailed learning analytics
- Performance benchmarking
- Skills gap analysis
- Career readiness reports

**✅ Exclusive Perks**:
- Annual data science conference pass (virtual)
- Job board access (exclusive postings)
- Portfolio review service (1x/year)
- Mentor matching program

---

## Feature Matrix

| Feature | Basic ($97) | Intermediate ($247) | Advanced ($497) |
|---------|-------------|---------------------|-----------------|
| **Courses** | 5 fundamental | 8 courses | All 9 courses |
| **Video Quality** | 720p stream | 1080p stream + download | 4K stream + unlimited download |
| **Video Download** | ❌ | ✅ (50GB/month) | ✅ (Unlimited) |
| **Slide Viewing** | ✅ View only | ✅ View + PDF download | ✅ View + PDF + PPTX |
| **Labs** | View-only | Interactive (100h/month) | Interactive (Unlimited + Custom) |
| **AI Tutor** | ❌ | ✅ (50 Q/month) | ✅ (Unlimited) |
| **Code Downloads** | ❌ | ✅ (5GB/month) | ✅ (Unlimited) |
| **Certificates** | ❌ | ✅ Digital | ✅ Blockchain-verified |
| **Support** | Email (48h) | Email (24h) + Forums | Priority (4h) + Video calls |
| **Community** | ❌ | ✅ | ✅ + Mentor matching |
| **Analytics** | Basic progress | Enhanced insights | Advanced analytics |
| **Offline Access** | ❌ | Videos + Slides | Full offline packages |

---

## Implementation

### Feature Checking Function

```python
from enum import Enum
from typing import List

class Tier(str, Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Feature(str, Enum):
    # Video features
    VIDEO_DOWNLOAD = "video_download"
    VIDEO_720P = "video_720p"
    VIDEO_1080P = "video_1080p"
    VIDEO_4K = "video_4k"
    
    # Slide features
    SLIDE_VIEW = "slide_view"
    SLIDE_PDF_DOWNLOAD = "slide_pdf_download"
    SLIDE_PPTX_DOWNLOAD = "slide_pptx_download"
    
    # Lab features
    LAB_VIEW = "lab_view"
    LAB_INTERACTIVE = "lab_interactive"
    LAB_CUSTOM_SCENARIOS = "lab_custom_scenarios"
    LAB_GPU_ACCESS = "lab_gpu_access"
    
    # AI features
    AI_TUTOR = "ai_tutor"
    AI_TUTOR_UNLIMITED = "ai_tutor_unlimited"
    
    # Download features
    CODE_DOWNLOAD = "code_download"
    DATASET_DOWNLOAD = "dataset_download"
    
    # Certificate features
    CERTIFICATE_DIGITAL = "certificate_digital"
    CERTIFICATE_BLOCKCHAIN = "certificate_blockchain"
    
    # Support features
    PRIORITY_SUPPORT = "priority_support"
    VIDEO_SUPPORT = "video_support"
    
    # Community features
    COMMUNITY_FORUMS = "community_forums"
    MENTOR_MATCHING = "mentor_matching"

# Feature matrix mapping
FEATURE_MATRIX = {
    Feature.VIDEO_DOWNLOAD: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.VIDEO_720P: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.VIDEO_1080P: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.VIDEO_4K: [Tier.ADVANCED],
    
    Feature.SLIDE_VIEW: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.SLIDE_PDF_DOWNLOAD: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.SLIDE_PPTX_DOWNLOAD: [Tier.ADVANCED],
    
    Feature.LAB_VIEW: [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.LAB_INTERACTIVE: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.LAB_CUSTOM_SCENARIOS: [Tier.ADVANCED],
    Feature.LAB_GPU_ACCESS: [Tier.ADVANCED],
    
    Feature.AI_TUTOR: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.AI_TUTOR_UNLIMITED: [Tier.ADVANCED],
    
    Feature.CODE_DOWNLOAD: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.DATASET_DOWNLOAD: [Tier.INTERMEDIATE, Tier.ADVANCED],
    
    Feature.CERTIFICATE_DIGITAL: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.CERTIFICATE_BLOCKCHAIN: [Tier.ADVANCED],
    
    Feature.PRIORITY_SUPPORT: [Tier.ADVANCED],
    Feature.VIDEO_SUPPORT: [Tier.ADVANCED],
    
    Feature.COMMUNITY_FORUMS: [Tier.INTERMEDIATE, Tier.ADVANCED],
    Feature.MENTOR_MATCHING: [Tier.ADVANCED],
}

def check_feature_access(user_tier: Tier, feature: Feature) -> bool:
    """
    Check if user's tier allows access to a specific feature.
    
    Args:
        user_tier: User's subscription tier
        feature: Feature to check access for
        
    Returns:
        bool: True if user has access, False otherwise
    """
    allowed_tiers = FEATURE_MATRIX.get(feature, [])
    return user_tier in allowed_tiers

def get_required_tier(feature: Feature) -> Tier:
    """
    Get the minimum tier required for a feature.
    
    Args:
        feature: Feature to check
        
    Returns:
        Tier: Minimum tier required (or None if not available)
    """
    allowed_tiers = FEATURE_MATRIX.get(feature, [])
    if not allowed_tiers:
        return None
    
    # Return the lowest tier that has access
    tier_order = [Tier.BASIC, Tier.INTERMEDIATE, Tier.ADVANCED]
    for tier in tier_order:
        if tier in allowed_tiers:
            return tier
    
    return None

def get_features_for_tier(user_tier: Tier) -> List[Feature]:
    """
    Get all features available for a tier.
    
    Args:
        user_tier: User's subscription tier
        
    Returns:
        List[Feature]: List of accessible features
    """
    features = []
    for feature, allowed_tiers in FEATURE_MATRIX.items():
        if user_tier in allowed_tiers:
            features.append(feature)
    return features
```

### Course Access Control

```python
# Course tier requirements
COURSE_TIER_REQUIREMENTS = {
    "01_DataScientistToolbox": Tier.BASIC,
    "02_RProgramming": Tier.BASIC,
    "03_GettingData": Tier.BASIC,
    "04_ExploratoryAnalysis": Tier.BASIC,
    "05_ReproducibleResearch": Tier.BASIC,
    "06_StatisticalInference": Tier.INTERMEDIATE,
    "07_RegressionModels": Tier.INTERMEDIATE,
    "08_PracticalMachineLearning": Tier.INTERMEDIATE,
    "09_DevelopingDataProducts": Tier.ADVANCED,
}

def check_course_access(user_tier: Tier, course_id: str) -> bool:
    """
    Check if user's tier allows access to a specific course.
    
    Args:
        user_tier: User's subscription tier
        course_id: Course identifier
        
    Returns:
        bool: True if user has access, False otherwise
    """
    required_tier = COURSE_TIER_REQUIREMENTS.get(course_id)
    if not required_tier:
        return False
    
    tier_hierarchy = {
        Tier.BASIC: 1,
        Tier.INTERMEDIATE: 2,
        Tier.ADVANCED: 3
    }
    
    return tier_hierarchy[user_tier] >= tier_hierarchy[required_tier]

def get_available_courses(user_tier: Tier) -> List[str]:
    """
    Get list of courses available to user based on tier.
    
    Args:
        user_tier: User's subscription tier
        
    Returns:
        List[str]: List of accessible course IDs
    """
    available = []
    for course_id in COURSE_TIER_REQUIREMENTS:
        if check_course_access(user_tier, course_id):
            available.append(course_id)
    return available
```

### Quota Management

```python
from datetime import datetime, timedelta
from typing import Optional
import redis

class QuotaManager:
    """Manage usage quotas for tier-limited features."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def get_ai_quota(self, user_id: str, user_tier: Tier) -> dict:
        """
        Get AI tutor quota information for user.
        
        Returns:
            dict: {
                "limit": int,           # Monthly limit (0 for Basic, 50 for Int, -1 for Adv)
                "used": int,            # Used this month
                "remaining": int,       # Remaining (-1 means unlimited)
                "reset_date": str       # ISO format date
            }
        """
        # Define limits
        quota_limits = {
            Tier.BASIC: 0,
            Tier.INTERMEDIATE: 50,
            Tier.ADVANCED: -1  # -1 means unlimited
        }
        
        limit = quota_limits[user_tier]
        
        # If Basic tier, return immediately
        if user_tier == Tier.BASIC:
            return {
                "limit": 0,
                "used": 0,
                "remaining": 0,
                "reset_date": None
            }
        
        # Get current month key
        month_key = datetime.now().strftime("%Y-%m")
        redis_key = f"ai_quota:{user_id}:{month_key}"
        
        # Get used count
        used = int(self.redis.get(redis_key) or 0)
        
        # Calculate remaining
        if limit == -1:  # Unlimited
            remaining = -1
        else:
            remaining = max(0, limit - used)
        
        # Calculate reset date (first day of next month)
        today = datetime.now()
        if today.month == 12:
            reset_date = datetime(today.year + 1, 1, 1)
        else:
            reset_date = datetime(today.year, today.month + 1, 1)
        
        return {
            "limit": limit,
            "used": used,
            "remaining": remaining,
            "reset_date": reset_date.isoformat()
        }
    
    def consume_ai_quota(self, user_id: str, user_tier: Tier) -> bool:
        """
        Attempt to consume one AI question from quota.
        
        Returns:
            bool: True if quota consumed successfully, False if quota exceeded
        """
        quota_info = self.get_ai_quota(user_id, user_tier)
        
        # Check if unlimited
        if quota_info["remaining"] == -1:
            # Still track usage for analytics
            month_key = datetime.now().strftime("%Y-%m")
            redis_key = f"ai_quota:{user_id}:{month_key}"
            self.redis.incr(redis_key)
            return True
        
        # Check if quota available
        if quota_info["remaining"] <= 0:
            return False
        
        # Consume quota
        month_key = datetime.now().strftime("%Y-%m")
        redis_key = f"ai_quota:{user_id}:{month_key}"
        self.redis.incr(redis_key)
        
        # Set expiry to end of next month (in case of key creation)
        expire_days = 60  # ~2 months
        self.redis.expire(redis_key, expire_days * 24 * 60 * 60)
        
        return True
    
    def get_download_quota(self, user_id: str, user_tier: Tier) -> dict:
        """
        Get download quota information for user.
        
        Returns:
            dict: {
                "limit_gb": float,      # Monthly limit in GB
                "used_gb": float,       # Used this month in GB
                "remaining_gb": float,  # Remaining in GB
                "reset_date": str
            }
        """
        # Define limits (in GB)
        quota_limits = {
            Tier.BASIC: 0,
            Tier.INTERMEDIATE: 50,
            Tier.ADVANCED: -1  # Unlimited
        }
        
        limit = quota_limits[user_tier]
        
        if user_tier == Tier.BASIC:
            return {
                "limit_gb": 0,
                "used_gb": 0,
                "remaining_gb": 0,
                "reset_date": None
            }
        
        # Get current month key
        month_key = datetime.now().strftime("%Y-%m")
        redis_key = f"download_quota:{user_id}:{month_key}"
        
        # Get used bytes, convert to GB
        used_bytes = int(self.redis.get(redis_key) or 0)
        used_gb = used_bytes / (1024 ** 3)
        
        # Calculate remaining
        if limit == -1:  # Unlimited
            remaining_gb = -1
        else:
            remaining_gb = max(0, limit - used_gb)
        
        # Calculate reset date
        today = datetime.now()
        if today.month == 12:
            reset_date = datetime(today.year + 1, 1, 1)
        else:
            reset_date = datetime(today.year, today.month + 1, 1)
        
        return {
            "limit_gb": limit,
            "used_gb": round(used_gb, 2),
            "remaining_gb": round(remaining_gb, 2) if remaining_gb != -1 else -1,
            "reset_date": reset_date.isoformat()
        }
    
    def consume_download_quota(self, user_id: str, user_tier: Tier, 
                               file_size_bytes: int) -> bool:
        """
        Attempt to consume download quota.
        
        Args:
            user_id: User identifier
            user_tier: User's tier
            file_size_bytes: Size of file to download in bytes
            
        Returns:
            bool: True if download allowed, False if quota exceeded
        """
        quota_info = self.get_download_quota(user_id, user_tier)
        
        # Check if unlimited
        if quota_info["remaining_gb"] == -1:
            # Still track usage
            month_key = datetime.now().strftime("%Y-%m")
            redis_key = f"download_quota:{user_id}:{month_key}"
            self.redis.incrby(redis_key, file_size_bytes)
            return True
        
        # Check if enough quota
        file_size_gb = file_size_bytes / (1024 ** 3)
        if file_size_gb > quota_info["remaining_gb"]:
            return False
        
        # Consume quota
        month_key = datetime.now().strftime("%Y-%m")
        redis_key = f"download_quota:{user_id}:{month_key}"
        self.redis.incrby(redis_key, file_size_bytes)
        self.redis.expire(redis_key, 60 * 24 * 60 * 60)  # 60 days
        
        return True
```

---

## UI/UX for Feature Gating

### Upgrade Prompts

**Design Principles**:
- Non-intrusive but visible
- Clear value proposition
- Single call-to-action (CTA)
- Show what they're missing

**Prompt Examples**:

```python
# Video download button (disabled for Basic)
"""
┌─────────────────────────────────┐
│  [🔒 Download Video]             │
│  Available in Intermediate tier  │
│  [Upgrade Now →]                 │
└─────────────────────────────────┘
"""

# AI Tutor (not available for Basic)
"""
┌─────────────────────────────────────┐
│  🤖 AI Tutor                         │
│  Get instant answers to your         │
│  questions!                          │
│                                      │
│  ✓ Context-aware assistance          │
│  ✓ Code debugging help               │
│  ✓ Concept clarification             │
│                                      │
│  Available in Intermediate tier      │
│  [Start Free Trial →]                │
└─────────────────────────────────────┘
"""

# Lab interactive mode (disabled for Basic)
"""
┌─────────────────────────────────────┐
│  This is a view-only preview         │
│                                      │
│  Upgrade to Intermediate to:         │
│  ✓ Edit and run code                 │
│  ✓ Complete hands-on exercises       │
│  ✓ Save your work                    │
│                                      │
│  [Unlock Interactive Labs →]         │
└─────────────────────────────────────┘
"""

# Quota exceeded (AI Tutor)
"""
┌─────────────────────────────────────┐
│  📊 AI Tutor Quota                   │
│  You've used all 50 questions this   │
│  month. Resets on Feb 1, 2024.       │
│                                      │
│  Upgrade to Advanced for:            │
│  ✓ Unlimited questions               │
│  ✓ Advanced AI models                │
│  ✓ Priority responses                │
│                                      │
│  [Upgrade to Advanced →]             │
└─────────────────────────────────────┘
"""
```

### Locked Course Cards

```html
<!-- Locked course (above user's tier) -->
<div class="course-card locked">
  <div class="course-image">
    <img src="course-thumb.jpg" alt="Course thumbnail" />
    <div class="lock-overlay">
      <span class="lock-icon">🔒</span>
    </div>
  </div>
  <div class="course-info">
    <h3>Developing Data Products</h3>
    <p class="tier-requirement">Requires Advanced Tier</p>
    <p class="course-description">
      Build data science applications with R and Shiny...
    </p>
    <button class="upgrade-btn">
      Unlock with Advanced →
    </button>
  </div>
</div>
```

### Feature Comparison Table (in Upgrade Page)

```
┌───────────────────────────────────────────────────────────────┐
│  Choose Your Plan                                              │
├───────────┬─────────────┬─────────────────┬─────────────────┤
│  Feature  │ Basic       │ Intermediate    │ Advanced        │
│           │ $97/year    │ $247/year       │ $497/year       │
├───────────┼─────────────┼─────────────────┼─────────────────┤
│  Courses  │ 5 courses   │ 8 courses       │ All 9 courses   │
│  Video    │ 720p stream │ 1080p + download│ 4K + unlimited  │
│  Labs     │ View-only   │ Interactive ✓   │ + Custom labs   │
│  AI Tutor │ ✗           │ 50 Q/month ✓    │ Unlimited ✓     │
│  Certif.  │ ✗           │ Digital ✓       │ Blockchain ✓    │
├───────────┼─────────────┼─────────────────┼─────────────────┤
│           │ [Current]   │ [Upgrade]       │ [Upgrade]       │
└───────────┴─────────────┴─────────────────┴─────────────────┘
```

---

## Testing Feature Gates

### Unit Tests

```python
import pytest
from feature_gating import check_feature_access, Tier, Feature

def test_basic_tier_video_access():
    assert check_feature_access(Tier.BASIC, Feature.VIDEO_720P) == True
    assert check_feature_access(Tier.BASIC, Feature.VIDEO_DOWNLOAD) == False
    assert check_feature_access(Tier.BASIC, Feature.VIDEO_4K) == False

def test_intermediate_tier_ai_tutor():
    assert check_feature_access(Tier.INTERMEDIATE, Feature.AI_TUTOR) == True
    assert check_feature_access(Tier.INTERMEDIATE, Feature.AI_TUTOR_UNLIMITED) == False

def test_advanced_tier_all_features():
    # Advanced tier should have access to all features
    for feature in Feature:
        assert check_feature_access(Tier.ADVANCED, feature) == True

def test_quota_management():
    from feature_gating import QuotaManager
    from unittest.mock import Mock
    
    redis_mock = Mock()
    redis_mock.get.return_value = b'45'  # User has used 45 questions
    
    quota_mgr = QuotaManager(redis_mock)
    quota_info = quota_mgr.get_ai_quota("user123", Tier.INTERMEDIATE)
    
    assert quota_info["limit"] == 50
    assert quota_info["used"] == 45
    assert quota_info["remaining"] == 5
```

### Integration Tests

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_video_download_blocked_for_basic():
    # Login as Basic tier user
    response = client.post("/api/auth/login", json={
        "license_key": "BASIC-123"
    })
    token = response.json()["access_token"]
    
    # Attempt to download video
    response = client.get(
        "/api/content/video/download/lesson-01",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403
    assert "upgrade" in response.json()["message"].lower()

def test_ai_tutor_quota_enforcement():
    # Login as Intermediate tier user
    response = client.post("/api/auth/login", json={
        "license_key": "INTERMEDIATE-456"
    })
    token = response.json()["access_token"]
    
    # Ask 50 questions (should succeed)
    for i in range(50):
        response = client.post(
            "/api/ai-tutor/ask",
            headers={"Authorization": f"Bearer {token}"},
            json={"question": f"Question {i}"}
        )
        assert response.status_code == 200
    
    # 51st question should fail
    response = client.post(
        "/api/ai-tutor/ask",
        headers={"Authorization": f"Bearer {token}"},
        json={"question": "Question 51"}
    )
    assert response.status_code == 429  # Too Many Requests
    assert "quota exceeded" in response.json()["message"].lower()
```

---

## Analytics & Monitoring

### Metrics to Track

**Feature Usage by Tier**:
- Video downloads (Intermediate/Advanced)
- AI tutor questions (Intermediate/Advanced)
- Lab launches (all tiers)
- Course enrollment (by tier)

**Conversion Opportunities**:
- Upgrade prompt impressions
- Upgrade prompt clicks
- Feature gate encounters (user tried locked feature)
- Quota exhaustion events

**User Behavior**:
- Time to first upgrade prompt encounter
- Most common blocked features
- Tier upgrade conversion rate
- Feature adoption rate by tier

### Sample Dashboard Queries

```sql
-- Feature gate encounters by tier and feature
SELECT 
    user_tier,
    feature_attempted,
    COUNT(*) as encounters,
    COUNT(DISTINCT user_id) as unique_users
FROM feature_gate_log
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY user_tier, feature_attempted
ORDER BY encounters DESC;

-- Upgrade conversion rate
SELECT 
    previous_tier,
    new_tier,
    COUNT(*) as upgrades,
    AVG(days_before_upgrade) as avg_days
FROM tier_changes
WHERE created_at >= NOW() - INTERVAL '90 days'
GROUP BY previous_tier, new_tier;

-- AI Tutor quota exhaustion rate
SELECT 
    user_tier,
    COUNT(DISTINCT user_id) as total_users,
    COUNT(DISTINCT CASE WHEN questions_used >= quota_limit THEN user_id END) as exhausted_users,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN questions_used >= quota_limit THEN user_id END) / COUNT(DISTINCT user_id), 2) as exhaustion_rate
FROM ai_tutor_usage
WHERE month = DATE_TRUNC('month', NOW())
GROUP BY user_tier;
```

---

## Future Enhancements

**Dynamic Feature Flags**:
- A/B testing different tier configurations
- Temporary feature unlocks (promotions)
- Grace periods (recently downgraded users)

**Personalized Upgrade Prompts**:
- ML-based targeting (predict which feature user wants most)
- Usage-based messaging (e.g., "You've viewed 10 labs - ready to try them?")
- Time-based offers (e.g., "Upgrade now and save 20%")

**Fair Usage Policies**:
- Soft limits with warnings before hard cutoff
- Rollover of unused quota (up to 20%)
- Family/team plans with shared quotas

**Granular Permissions**:
- Course-specific access grants
- Time-limited feature trials
- Scholarship/grant tiers with custom access

---

## Conclusion

The feature gating system is designed to:

1. **Create Clear Value Tiers**: Each tier offers substantial new value
2. **Encourage Upgrades**: Strategic feature placement drives conversions
3. **Maintain User Satisfaction**: All tiers get a complete, useful experience
4. **Be Technically Robust**: Real-time enforcement with caching for performance
5. **Support Analytics**: Track usage and optimize tier definitions

This system balances business goals (revenue) with user experience (value and accessibility).
