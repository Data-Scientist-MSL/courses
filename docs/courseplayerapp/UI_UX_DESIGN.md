# CoursePlayerApp - UI/UX Design Specification

## Overview

CoursePlayerApp uses Streamlit to deliver an intuitive, responsive learning interface. This document defines the page structure, navigation flows, component designs, and user experience patterns.

---

## Design Principles

### 1. Learning-First
- Minimize clicks to reach content
- Keep navigation always visible
- Progress indicators everywhere
- Clear next steps

### 2. Tier-Aware
- Show locked features with upgrade prompts (not hidden)
- Use visual cues (🔒 icon, dimmed colors) for unavailable features
- Progressive disclosure: Basic sees what they're missing

### 3. Responsive & Accessible
- Mobile-friendly layouts
- Keyboard navigation support
- High contrast ratios (WCAG 2.1 AA)
- Screen reader compatible

### 4. Performance
- Lazy loading for course lists
- Cached API responses
- Progressive image loading

---

## Page Structure

### Streamlit Multi-Page App Structure

```
CoursePlayerApp/
├── Home.py                        # Entry point (login or redirect to dashboard)
└── pages/
    ├── 1_🏠_Dashboard.py         # Main dashboard
    ├── 2_📚_My_Courses.py        # Course catalog
    ├── 3_🎓_Course_Player.py     # Video/slides/labs player
    ├── 4_🧪_Labs.py              # Lab listing and launcher
    ├── 5_📊_My_Progress.py       # Progress analytics
    ├── 6_🎖️_Certificates.py     # Certificate gallery
    └── 7_⚙️_Settings.py          # User settings
```

**Navigation**: Streamlit sidebar automatically shows all pages

---

## Page Designs

### Page 1: Home (Login)

**File**: `Home.py`

**Purpose**: Authenticate users via license key

**Layout**:
```
┌────────────────────────────────────────┐
│  🎓 GAI-Observe Academy                │
│                                        │
│  Welcome to Your Learning Journey!     │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │  Enter License Key:              │ │
│  │  ┌────────────────────────────┐  │ │
│  │  │ XXXX-XXXX-XXXX-XXXX        │  │ │
│  │  └────────────────────────────┘  │ │
│  │                                  │ │
│  │  [    Login    ]                 │ │
│  └──────────────────────────────────┘ │
│                                        │
│  Don't have a license?                 │
│  [Purchase Now] [Contact Support]      │
└────────────────────────────────────────┘
```

**Implementation**:
```python
# Home.py
import streamlit as st
from utils.auth import authenticate

st.set_page_config(
    page_title="GAI-Observe Academy",
    page_icon="🎓",
    layout="centered"
)

# Check if already authenticated
if st.session_state.get("authenticated"):
    st.switch_page("pages/1_🏠_Dashboard.py")

# Login page
st.title("🎓 GAI-Observe Academy")
st.subheader("Welcome to Your Learning Journey!")

with st.container():
    st.markdown("---")
    
    license_key = st.text_input(
        "Enter your license key:",
        type="password",
        placeholder="XXXX-XXXX-XXXX-XXXX",
        help="License key provided after purchase"
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔐 Login", type="primary"):
            if license_key:
                with st.spinner("Validating license..."):
                    success = authenticate(license_key)
                    if success:
                        st.success("✅ Login successful!")
                        time.sleep(1)
                        st.switch_page("pages/1_🏠_Dashboard.py")
            else:
                st.error("Please enter your license key")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[💳 Purchase License](https://payment.gai-observe.com)")
    with col2:
        st.markdown("[📧 Contact Support](mailto:support@gai-observe.com)")
```

---

### Page 2: Dashboard

**File**: `pages/1_🏠_Dashboard.py`

**Purpose**: Overview of user's learning status and quick actions

**Layout**:
```
┌────────────────────────────────────────────────────────┐
│ Welcome back, [Name]! 👋        [Tier Badge: Advanced] │
├────────────────────────────────────────────────────────┤
│                                                        │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│ │ Courses     │ │ Completion  │ │ Certificates │      │
│ │ In Progress │ │ Rate        │ │ Earned       │      │
│ │     3       │ │    67%      │ │      2       │      │
│ └─────────────┘ └─────────────┘ └─────────────┘      │
│                                                        │
│ 📚 Continue Learning                                   │
│ ┌────────────────────────────────────────────────┐    │
│ │ NLP with Transformers                    67%   │    │
│ │ Module 3: Attention Mechanisms                 │    │
│ │ [Continue →]                                   │    │
│ └────────────────────────────────────────────────┘    │
│                                                        │
│ 🎯 Recommended Next Steps                             │
│ • Complete Module 3 Quiz (unlock Module 4)            │
│ • Start Lab 3: Build Attention Layer                  │
│ • Review slides for key concepts                      │
│                                                        │
│ 🔥 Learning Streak: 7 days                            │
│ ███████░░░ (Keep it going!)                           │
└────────────────────────────────────────────────────────┘
```

**Implementation**:
```python
# pages/1_🏠_Dashboard.py
import streamlit as st
from utils.progress_tracker import ProgressTracker
from components.course_card import render_continue_learning_card

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

# Auth check
if not st.session_state.get("authenticated"):
    st.switch_page("Home.py")

user_id = st.session_state.get("user_id")
tier = st.session_state.get("tier")
email = st.session_state.get("email")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title(f"Welcome back, {email.split('@')[0]}! 👋")
with col2:
    tier_colors = {"basic": "gray", "intermediate": "blue", "advanced": "gold"}
    st.markdown(f"**Tier:** :{tier_colors[tier]}[{tier.title()}]")

st.divider()

# Key metrics
tracker = ProgressTracker(user_id)
stats = tracker.get_overall_stats()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Courses In Progress", stats['courses_in_progress'])

with col2:
    st.metric("Avg Completion", f"{stats['avg_completion']}%")

with col3:
    st.metric("Certificates Earned", stats['certificates_earned'])

with col4:
    st.metric("Learning Streak", f"{stats['learning_streak']} days", delta="🔥")

st.divider()

# Continue learning
st.subheader("📚 Continue Learning")
current_course = tracker.get_current_course()
if current_course:
    render_continue_learning_card(current_course)
else:
    st.info("No courses in progress. Browse the catalog to get started!")
    if st.button("Browse Courses"):
        st.switch_page("pages/2_📚_My_Courses.py")

st.divider()

# Recommended next steps
st.subheader("🎯 Recommended Next Steps")
recommendations = tracker.get_recommendations()
for rec in recommendations:
    st.markdown(f"• {rec}")

# Learning streak
st.divider()
st.subheader(f"🔥 Learning Streak: {stats['learning_streak']} days")
st.progress(min(stats['learning_streak'] / 30, 1.0))
st.caption("Learn for 30 consecutive days to unlock the 'Month Master' badge!")
```

---

### Page 3: My Courses

**File**: `pages/2_📚_My_Courses.py`

**Purpose**: Browse and access courses

**Layout**:
```
┌────────────────────────────────────────────────────────┐
│ 📚 My Courses                                          │
├────────────────────────────────────────────────────────┤
│ [🔍 Search] [Category ▼] [Difficulty ▼] [Sort ▼]       │
│                                                        │
│ Your Courses (8 accessible)                            │
│ ┌────────┐ ┌────────┐ ┌────────┐                      │
│ │ Course │ │ Course │ │ Course │                      │
│ │   1    │ │   2    │ │   3    │                      │
│ │ [67%]  │ │ [100%] │ │ [12%]  │                      │
│ │Continue│ │ Review │ │ Start  │                      │
│ └────────┘ └────────┘ └────────┘                      │
│                                                        │
│ Locked Courses (1) 🔒                                  │
│ ┌────────┐                                             │
│ │Advanced│                                             │
│ │Deep    │  Requires Advanced Tier                    │
│ │Learning│  [Upgrade →]                               │
│ └────────┘                                             │
└────────────────────────────────────────────────────────┘
```

**Implementation**:
```python
# pages/2_📚_My_Courses.py
import streamlit as st
from utils.api_client import CoursesGTMClient
from utils.feature_flags import FeatureFlags
from components.course_card import render_course_card

st.set_page_config(page_title="My Courses", page_icon="📚", layout="wide")

# Auth check
if not st.session_state.get("authenticated"):
    st.switch_page("Home.py")

st.title("📚 My Courses")

# Filters
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:
    search = st.text_input("🔍 Search courses", placeholder="Search by title or topic...")

with col2:
    category = st.selectbox("Category", ["All", "AI", "Data Science", "Machine Learning"])

with col3:
    difficulty = st.selectbox("Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])

with col4:
    sort_by = st.selectbox("Sort by", ["Recently Accessed", "Progress", "Alphabetical"])

st.divider()

# Fetch courses
gtm_client = CoursesGTMClient()
token = st.session_state.get("token")
all_courses = gtm_client.get_courses(token)

# Filter accessible vs locked
tier = st.session_state.get("tier")
accessible_courses = FeatureFlags.get_course_access(tier)

accessible = [c for c in all_courses if c['id'] in accessible_courses]
locked = [c for c in all_courses if c['id'] not in accessible_courses]

# Render accessible courses
st.subheader(f"Your Courses ({len(accessible)} accessible)")
cols = st.columns(3)

for i, course in enumerate(accessible):
    with cols[i % 3]:
        render_course_card(course, accessible=True)

# Render locked courses
if locked:
    st.divider()
    st.subheader(f"🔒 Unlock More Courses ({len(locked)})")
    cols = st.columns(3)
    
    for i, course in enumerate(locked):
        with cols[i % 3]:
            render_course_card(course, accessible=False)
```

---

### Page 4: Course Player

**File**: `pages/3_🎓_Course_Player.py`

**Purpose**: Watch videos, view slides, read content

**Layout**:
```
┌──────────────┬──────────────────────────┬──────────────┐
│  Module Nav  │   Video/Slides Player    │  AI Tutor    │
│              │                          │              │
│ ✅ Module 1  │  ┌──────────────────┐    │ 🤖 Ask me    │
│ ⏳ Module 2  │  │                  │    │ anything!    │
│ 🔒 Module 3  │  │   Video Player   │    │              │
│              │  │                  │    │ [Question?]  │
│ Videos:      │  └──────────────────┘    │ [  Send  ]   │
│ • Intro ✅   │                          │              │
│ • Concept ▶  │  [⏯️] [🔊] [⚙️] [⬇️]     │ Recent:      │
│              │                          │ • What is    │
│ Slides: 📄   │  📝 Transcript           │   NLP?       │
│ Lab: 🧪      │  Lorem ipsum dolor...    │              │
│ Quiz: ❓     │                          │              │
└──────────────┴──────────────────────────┴──────────────┘
```

**Implementation**:
```python
# pages/3_🎓_Course_Player.py
import streamlit as st
from components.video_player import render_video_player
from components.slides_viewer import render_slides_viewer
from components.ai_tutor_chat import render_ai_tutor

st.set_page_config(page_title="Course Player", page_icon="🎓", layout="wide")

# Auth check
if not st.session_state.get("authenticated"):
    st.switch_page("Home.py")

# Get current course
course_id = st.session_state.get("current_course")
if not course_id:
    st.warning("No course selected. Please select a course first.")
    if st.button("Browse Courses"):
        st.switch_page("pages/2_📚_My_Courses.py")
    st.stop()

# Fetch course data
gtm_client = CoursesGTMClient()
course = gtm_client.get_course_details(course_id, st.session_state.get("token"))

st.title(course['title'])
st.caption(course['description'])

# Layout: Sidebar (navigation) + Main (player) + Sidebar (AI Tutor)
col1, col2, col3 = st.columns([1, 3, 1])

# Left: Module navigation
with col1:
    st.subheader("📑 Modules")
    for module in course['modules']:
        module_status = get_module_status(module)  # ✅ ⏳ 🔒
        
        with st.expander(f"{module_status} {module['title']}", expanded=False):
            for video in module['videos']:
                if st.button(f"📹 {video['title']}", key=f"video_{video['id']}"):
                    st.session_state['current_video'] = video
                    st.rerun()
            
            if module.get('slides'):
                if st.button(f"📄 Slides", key=f"slides_{module['id']}"):
                    st.session_state['current_view'] = 'slides'
                    st.session_state['current_slides'] = module['slides']
                    st.rerun()
            
            if module.get('lab'):
                if st.button(f"🧪 Lab", key=f"lab_{module['id']}"):
                    st.session_state['current_view'] = 'lab'
                    st.session_state['current_lab'] = module['lab']
                    st.rerun()

# Center: Content player
with col2:
    current_view = st.session_state.get("current_view", "video")
    
    if current_view == "video":
        current_video = st.session_state.get("current_video")
        if current_video:
            render_video_player(
                video_id=current_video['id'],
                video_url=current_video['video_url'],
                tier=st.session_state.get("tier")
            )
        else:
            st.info("Select a video from the module navigation")
    
    elif current_view == "slides":
        current_slides = st.session_state.get("current_slides")
        render_slides_viewer(current_slides, tier=st.session_state.get("tier"))
    
    elif current_view == "lab":
        current_lab = st.session_state.get("current_lab")
        render_lab_launcher(current_lab, tier=st.session_state.get("tier"))

# Right: AI Tutor
with col3:
    render_ai_tutor()
```

---

### Page 5: Labs

**File**: `pages/4_🧪_Labs.py`

**Purpose**: List all labs with status and launch links

**Layout**:
```
┌────────────────────────────────────────────────────────┐
│ 🧪 Labs                                                │
├────────────────────────────────────────────────────────┤
│ Course: NLP with Transformers                          │
│                                                        │
│ ┌────────────────────────────────────────────────┐    │
│ │ Lab 1: Tokenization Basics             ✅ 95%  │    │
│ │ Duration: 60 min                               │    │
│ │ [Review Results]                               │    │
│ └────────────────────────────────────────────────┘    │
│                                                        │
│ ┌────────────────────────────────────────────────┐    │
│ │ Lab 2: Build Attention Layer           ⏳ 0%   │    │
│ │ Duration: 90 min                               │    │
│ │ [🚀 Start Lab]                                 │    │
│ └────────────────────────────────────────────────┘    │
│                                                        │
│ ┌────────────────────────────────────────────────┐    │
│ │ Lab 3: Fine-tune BERT                  🔒      │    │
│ │ Requires: Complete Module 3 Quiz               │    │
│ │ [Locked]                                       │    │
│ └────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────┘
```

---

### Page 6: My Progress

**File**: `pages/5_📊_My_Progress.py`

**Purpose**: Detailed analytics and visualizations

**Layout**:
```
┌────────────────────────────────────────────────────────┐
│ 📊 My Progress                                         │
├────────────────────────────────────────────────────────┤
│ [Course Dropdown ▼] [Export CSV]                      │
│                                                        │
│ Overall Progress: 67%                                  │
│ ████████████████░░░░░░░░░░                            │
│                                                        │
│ Time Spent (Last 30 Days)                             │
│ ┌────────────────────────────────────────────────┐    │
│ │     📈 Line Chart                              │    │
│ │                                                │    │
│ └────────────────────────────────────────────────┘    │
│                                                        │
│ Quiz Performance                                       │
│ ┌────────────────────────────────────────────────┐    │
│ │     📊 Bar Chart                               │    │
│ │                                                │    │
│ └────────────────────────────────────────────────┘    │
│                                                        │
│ [Advanced Tier Only] Activity Heatmap                  │
│ ┌────────────────────────────────────────────────┐    │
│ │     🔥 Heatmap (GitHub-style)                  │    │
│ └────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────┘
```

---

### Page 7: Certificates

**File**: `pages/6_🎖️_Certificates.py`

**Purpose**: View and share earned certificates

**Layout**:
```
┌────────────────────────────────────────────────────────┐
│ 🎖️ My Certificates                                    │
├────────────────────────────────────────────────────────┤
│ You've earned 2 certificates! 🎉                      │
│                                                        │
│ ┌───────────┐  ┌───────────┐                          │
│ │           │  │           │                          │
│ │Certificate│  │Certificate│                          │
│ │    AI     │  │    NLP    │                          │
│ │           │  │           │                          │
│ │ [Download]│  │ [Download]│                          │
│ │ [LinkedIn]│  │ [LinkedIn]│                          │
│ │ [Verify]  │  │ [Verify]  │                          │
│ └───────────┘  └───────────┘                          │
│                                                        │
│ 🔓 Unlock More Certificates                            │
│ • Complete "Deep Learning" to earn your next cert     │
│ • 80% course completion required                      │
└────────────────────────────────────────────────────────┘
```

---

### Page 8: Settings

**File**: `pages/7_⚙️_Settings.py`

**Purpose**: User preferences and account management

**Layout**:
```
┌────────────────────────────────────────────────────────┐
│ ⚙️ Settings                                            │
├────────────────────────────────────────────────────────┤
│ Profile                                                │
│ Email: student@example.com                             │
│ User ID: uuid-v4                                       │
│                                                        │
│ Subscription                                           │
│ Current Tier: Intermediate                             │
│ License Expires: 2027-01-12                            │
│ [⬆️ Upgrade to Advanced]                              │
│                                                        │
│ Preferences                                            │
│ ☑️ Email notifications                                 │
│ ☐ Weekly progress report                              │
│ ☑️ Auto-resume videos                                  │
│                                                        │
│ Accessibility                                          │
│ [ ] High contrast mode                                 │
│ [ ] Dyslexia-friendly font                             │
│ Caption language: English ▼                            │
│                                                        │
│ [Save Changes]                                         │
│ [Logout]                                               │
└────────────────────────────────────────────────────────┘
```

---

## Component Library

### Reusable Components

#### Course Card
```python
# components/course_card.py
def render_course_card(course: dict, accessible: bool = True):
    """Render a course card (accessible or locked)"""
    if accessible:
        st.image(course['thumbnail'], use_column_width=True)
        st.markdown(f"**{course['title']}**")
        st.caption(course['instructor']['name'])
        
        progress = get_course_progress(course['id'])
        st.progress(progress / 100)
        st.caption(f"{progress}% complete")
        
        if st.button("Continue Learning", key=f"course_{course['id']}"):
            st.session_state['current_course'] = course['id']
            st.switch_page("pages/3_🎓_Course_Player.py")
    else:
        # Locked state
        st.image(course['thumbnail'], use_column_width=True)
        st.markdown(f"**{course['title']}** 🔒")
        st.caption(f"Requires {course['required_tier'].title()} tier")
        st.button("Upgrade to Unlock", disabled=True, key=f"locked_{course['id']}")
```

#### Progress Bar Component
```python
# components/progress_bar.py
def render_progress_bar(label: str, progress: int, color: str = "blue"):
    """Render animated progress bar"""
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"**{label}**")
        st.progress(progress / 100)
    with col2:
        st.metric("", f"{progress}%")
```

---

## Navigation Patterns

### Breadcrumb Navigation
```python
# utils/breadcrumbs.py
def render_breadcrumbs(path: list):
    """
    Render breadcrumb navigation
    
    Example: path = [("Home", "/"), ("Courses", "/courses"), ("AI-03", None)]
    """
    breadcrumb_html = " > ".join([
        f'<a href="{link}">{label}</a>' if link else label
        for label, link in path
    ])
    st.markdown(breadcrumb_html, unsafe_allow_html=True)
```

### Sidebar Navigation (Auto-generated by Streamlit)
Streamlit automatically creates sidebar navigation from pages folder structure.

---

## Responsive Design

### Mobile Layout Adjustments

```python
# Check viewport width (if custom CSS is used)
def is_mobile():
    """Detect mobile viewport (simplified)"""
    # Note: Streamlit doesn't natively detect viewport width
    # Use st.columns with responsive ratios instead
    return False  # Placeholder


# Adaptive columns
if is_mobile():
    cols = st.columns(1)  # Single column on mobile
else:
    cols = st.columns(3)  # Three columns on desktop
```

---

## Color Scheme & Theming

### Custom Theme (`config.toml`)
```toml
[theme]
primaryColor = "#4CAF50"          # Green (action buttons)
backgroundColor = "#FFFFFF"       # White
secondaryBackgroundColor = "#F0F0F0"  # Light gray
textColor = "#333333"             # Dark gray
font = "sans serif"

[tier_colors]
basic = "#9E9E9E"                 # Gray
intermediate = "#2196F3"          # Blue
advanced = "#FFD700"              # Gold
```

---

## Accessibility Features

See [ACCESSIBILITY.md](./ACCESSIBILITY.md) for full specification.

**Quick Summary**:
- Keyboard shortcuts for all actions
- ARIA labels on all interactive elements
- Focus indicators visible
- Color contrast ≥4.5:1

---

## Performance Optimizations

### Caching
```python
@st.cache_data(ttl=3600)
def fetch_course_catalog():
    """Cache course catalog for 1 hour"""
    return gtm_client.get_courses()


@st.cache_resource
def load_video_player():
    """Cache video player component"""
    return VideoPlayerComponent()
```

### Lazy Loading
```python
# Load images lazily
st.image(course['thumbnail'], use_column_width=True, lazy=True)

# Paginate course lists
page = st.number_input("Page", min_value=1, max_value=total_pages)
courses = fetch_courses(page=page, per_page=12)
```

---

## Testing UI Components

### Visual Regression Tests
```python
# tests/test_ui.py
def test_course_card_rendering(snapshot):
    """Test course card visual appearance"""
    mock_course = {"title": "Test Course", "thumbnail": "test.jpg"}
    rendered = render_course_card(mock_course)
    assert snapshot == rendered
```

---

## Conclusion

This UI/UX design ensures:
- **Intuitive navigation**: Clear page structure
- **Tier awareness**: Visible upgrade opportunities
- **Responsive**: Works on desktop and mobile
- **Accessible**: WCAG 2.1 AA compliant
- **Performant**: Cached data, lazy loading

The Streamlit framework provides rapid development while maintaining professional UI quality.
