# UI/UX Design Specification

## Overview

CoursePlayerApp's user interface is built with Streamlit, providing a clean, responsive, and intuitive learning experience. This specification defines the page structure, navigation, components, and design patterns used throughout the application.

---

## Design Philosophy

### Core Principles

1. **Simplicity First**: Clean, uncluttered interface with minimal cognitive load
2. **Progressive Disclosure**: Show advanced features as users upgrade tiers
3. **Accessibility**: WCAG 2.1 AA compliant for all users
4. **Consistency**: Unified design language across all pages
5. **Responsiveness**: Works on desktop, tablet, and mobile
6. **Performance**: Fast load times, lazy loading where appropriate

### Visual Style

- **Color Scheme**: Professional blue/white with accent colors
- **Typography**: Clean, readable fonts (Inter, Roboto)
- **Icons**: Emoji-based for Streamlit compatibility, consistent meanings
- **Spacing**: Generous whitespace, clear visual hierarchy
- **Feedback**: Immediate visual feedback for all interactions

---

## Page Structure

### Streamlit Multipage App Architecture

```
CoursePlayerApp/
├── Home.py                          # Main entry point (authentication)
└── pages/
    ├── 1_🏠_Dashboard.py           # User dashboard
    ├── 2_📚_My_Courses.py          # Course catalog
    ├── 3_🎓_Course_Player.py       # Main learning interface
    ├── 4_🧪_Labs.py                # Lab management
    ├── 5_📊_My_Progress.py         # Progress analytics
    ├── 6_🎖️_Certificates.py       # Certificate gallery
    └── 7_⚙️_Settings.py            # User settings
```

---

## Page Specifications

### 0. Home / Authentication (`Home.py`)

**Purpose**: Login and license validation

**Layout**:
```python
import streamlit as st
from utils.auth import authenticate

st.set_page_config(
    page_title="GAI-Observe Academy",
    page_icon="🎓",
    layout="centered"
)

# Check if already authenticated
if authenticate():
    st.switch_page("pages/1_🏠_Dashboard.py")

# Login interface
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("assets/logo.png", width=200)
    st.title("🎓 GAI-Observe Academy")
    st.markdown("---")
    
    st.subheader("Welcome Back!")
    
    license_key = st.text_input(
        "License Key",
        type="password",
        placeholder="LMSQ-XXXX-XXXX-XXXX-XXXX",
        help="Enter your license key from LemonSqueezy"
    )
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🔐 Login", type="primary", use_container_width=True):
            # Validate license
            pass
    
    with col_btn2:
        if st.button("🛒 Purchase License", use_container_width=True):
            st.link_button("Visit Store", "https://gai-observe.com/store")
    
    st.markdown("---")
    st.caption("Secure license-based authentication • No password required")
```

**Features**:
- Centered login form
- License key input (masked)
- Purchase link for new users
- Clean, professional design

---

### 1. Dashboard (`pages/1_🏠_Dashboard.py`)

**Purpose**: Overview of learning activity and quick access

**Layout**:

```python
import streamlit as st
from utils.progress import get_user_progress

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🏠 Dashboard")
    st.caption(f"Welcome back, {st.session_state['email'].split('@')[0].title()}!")
with col2:
    st.metric("Tier", st.session_state['tier'].title())

# Quick Stats
st.markdown("---")
st.subheader("📊 Your Learning at a Glance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Courses In Progress", "3", delta="+1 this month")
with col2:
    st.metric("Completion Rate", "67%", delta="+12%")
with col3:
    st.metric("Certificates Earned", "2")
with col4:
    st.metric("Current Streak", "7 days", delta="🔥")

# Continue Learning
st.markdown("---")
st.subheader("📚 Continue Learning")

progress = get_user_progress(st.session_state['user_id'])
recent_course = get_most_recent_course(progress)

if recent_course:
    with st.container():
        col1, col2, col3 = st.columns([2, 3, 1])
        
        with col1:
            st.image(recent_course['thumbnail_url'], use_column_width=True)
        
        with col2:
            st.markdown(f"**{recent_course['course_title']}**")
            st.progress(recent_course['overall_progress'] / 100)
            st.caption(f"{recent_course['overall_progress']}% complete • Last accessed: {recent_course['last_accessed']}")
        
        with col3:
            if st.button("▶️ Resume", type="primary", use_container_width=True):
                st.switch_page("pages/3_🎓_Course_Player.py")

# Recent Activity
st.markdown("---")
st.subheader("🕐 Recent Activity")

activities = get_recent_activities(st.session_state['user_id'])

for activity in activities[:5]:
    with st.expander(f"{activity['icon']} {activity['title']} • {activity['time_ago']}"):
        st.write(activity['description'])

# Upgrade CTA (if not Advanced)
if st.session_state['tier'] != 'advanced':
    st.markdown("---")
    st.info(f"🚀 Upgrade to unlock more features! [View Upgrade Options](settings)")
```

**Features**:
- Quick stats with deltas
- Continue learning shortcut
- Recent activity feed
- Upgrade CTA for non-Advanced users

---

### 2. My Courses (`pages/2_📚_My_Courses.py`)

**Purpose**: Browse and select courses

**Layout**:

```python
import streamlit as st
from utils.courses import get_accessible_courses, filter_courses

st.set_page_config(page_title="My Courses", page_icon="📚", layout="wide")

st.title("📚 My Courses")

# Filters
col1, col2, col3, col4 = st.columns([2, 1, 1, 2])

with col1:
    search = st.text_input("🔍 Search courses", placeholder="e.g., Machine Learning")

with col2:
    category = st.selectbox("Category", ["All", "AI", "Data Science", "ML"])

with col3:
    difficulty = st.selectbox("Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])

with col4:
    view_mode = st.radio("View", ["Grid", "List"], horizontal=True)

st.markdown("---")

# Course grid/list
courses = get_accessible_courses(st.session_state['tier'])
filtered = filter_courses(courses, search, category, difficulty)

if view_mode == "Grid":
    # Grid view (3 columns)
    cols = st.columns(3)
    
    for idx, course in enumerate(filtered):
        with cols[idx % 3]:
            render_course_card(course)

else:
    # List view
    for course in filtered:
        render_course_list_item(course)

def render_course_card(course: dict):
    """Render course card in grid view"""
    with st.container():
        st.image(course['thumbnail_url'], use_column_width=True)
        st.markdown(f"**{course['title']}**")
        st.caption(f"{course['difficulty']} • {course['duration_hours']}h")
        
        if course['accessible']:
            if course.get('progress', 0) > 0:
                st.progress(course['progress'] / 100)
                st.caption(f"{course['progress']}% complete")
            
            if st.button("▶️ Start", key=course['course_id'], use_container_width=True):
                st.session_state['current_course_id'] = course['course_id']
                st.switch_page("pages/3_🎓_Course_Player.py")
        else:
            st.warning(f"🔒 {course['tier_required'].title()} tier required")
            if st.button("Upgrade", key=f"upgrade_{course['course_id']}", use_container_width=True):
                st.switch_page("pages/7_⚙️_Settings.py")
```

**Features**:
- Search and filter functionality
- Grid/list view toggle
- Course cards with progress
- Locked courses with upgrade prompts

---

### 3. Course Player (`pages/3_🎓_Course_Player.py`)

**Purpose**: Main learning interface

**Layout**:

```python
import streamlit as st
from components.video_player import render_video_player
from components.ai_tutor_ui import render_ai_tutor_sidebar

st.set_page_config(page_title="Course Player", page_icon="🎓", layout="wide")

# Get current course
course_id = st.session_state.get('current_course_id')
course = get_course_details(course_id)

# Sidebar: Module navigation
with st.sidebar:
    st.title(course['title'])
    st.caption(course['instructor']['name'])
    
    st.markdown("---")
    st.subheader("📑 Modules")
    
    for module in course['modules']:
        with st.expander(f"{module['title']} ({module['progress']}%)"):
            # Videos
            for video in module['videos']:
                icon = "✅" if video.get('watched') else "▶️"
                if st.button(f"{icon} {video['title']}", key=video['video_id']):
                    st.session_state['current_video_id'] = video['video_id']
                    st.rerun()
            
            # Quiz
            if module.get('quiz'):
                if st.button(f"📝 {module['quiz']['title']}", key=module['quiz']['quiz_id']):
                    load_quiz(module['quiz']['quiz_id'])
    
    # AI Tutor (if enabled)
    render_ai_tutor_sidebar()

# Main content area
tab1, tab2, tab3 = st.tabs(["📹 Video", "📊 Slides", "ℹ️ Info"])

with tab1:
    video_id = st.session_state.get('current_video_id')
    if video_id:
        render_video_player(video_id, course_id, module_id)
    else:
        st.info("Select a video from the sidebar to start learning")

with tab2:
    render_slides_viewer()

with tab3:
    st.markdown(course['description'])
    st.markdown("**Prerequisites:**")
    for prereq in course.get('prerequisites', []):
        st.write(f"- {prereq}")

# Progress bar at bottom
st.markdown("---")
col1, col2 = st.columns([4, 1])

with col1:
    st.progress(course['progress'] / 100)
    st.caption(f"Course Progress: {course['progress']}%")

with col2:
    if st.button("📊 View Detailed Progress"):
        st.switch_page("pages/5_📊_My_Progress.py")
```

**Features**:
- Three-column layout (sidebar, main, AI tutor)
- Module navigation tree
- Tabbed content (video, slides, info)
- Real-time progress tracking
- AI Tutor integration in sidebar

---

### 4. Labs (`pages/4_🧪_Labs.py`)

**Purpose**: Lab management and launcher

**Layout**:

```python
import streamlit as st
from components.lab_launcher import render_lab_launcher

st.set_page_config(page_title="Labs", page_icon="🧪", layout="wide")

st.title("🧪 Interactive Labs")

# Course selector
course_id = st.selectbox(
    "Select Course",
    options=get_enrolled_courses(),
    format_func=lambda c: c['title']
)

course = get_course_details(course_id)

# Lab grid
st.markdown("---")

for module in course['modules']:
    if module.get('labs'):
        st.subheader(f"Module: {module['title']}")
        
        cols = st.columns(2)
        
        for idx, lab in enumerate(module['labs']):
            with cols[idx % 2]:
                render_lab_card(lab)

def render_lab_card(lab: dict):
    """Render lab card"""
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{lab['title']}**")
            st.caption(f"Difficulty: {lab['difficulty']}")
            
            if lab.get('status') == 'completed':
                st.success(f"✅ Completed • Score: {lab['score']}/{lab['max_score']}")
            elif lab.get('status') == 'in_progress':
                st.info("⏳ In Progress")
            else:
                st.caption("Not started")
        
        with col2:
            if lab.get('status') == 'completed':
                if st.button("🔄 Retry", key=f"retry_{lab['lab_id']}", use_container_width=True):
                    launch_lab(lab['lab_id'])
            else:
                if st.button("🚀 Start", key=f"start_{lab['lab_id']}", type="primary", use_container_width=True):
                    launch_lab(lab['lab_id'])
```

**Features**:
- Course filter
- Lab cards with status
- Launch buttons
- Completion tracking

---

### 5. My Progress (`pages/5_📊_My_Progress.py`)

**Purpose**: Detailed progress analytics

See PROGRESS_TRACKING.md for detailed implementation.

**Features**:
- Course progress charts
- Module breakdown
- Quiz/lab performance trends
- Time analytics (Intermediate+)
- Heatmap (Advanced only)
- Export capability (Advanced only)

---

### 6. Certificates (`pages/6_🎖️_Certificates.py`)

**Purpose**: Certificate gallery and sharing

**Layout**:

```python
import streamlit as st

st.set_page_config(page_title="Certificates", page_icon="🎖️", layout="wide")

st.title("🎖️ My Certificates")

certificates = get_user_certificates(st.session_state['user_id'])

if not certificates:
    st.info("🎯 No certificates yet. Complete a course to earn your first certificate!")
else:
    # Certificate grid
    cols = st.columns(3)
    
    for idx, cert in enumerate(certificates):
        with cols[idx % 3]:
            render_certificate_card(cert)

def render_certificate_card(cert: dict):
    """Render certificate card"""
    with st.container():
        st.image(cert['thumbnail_url'], use_column_width=True)
        st.markdown(f"**{cert['course_title']}**")
        st.caption(f"Issued: {cert['issued_date']}")
        st.caption(f"Score: {cert['final_score']}%")
        
        # Blockchain badge (Advanced tier)
        if cert.get('blockchain_verified'):
            st.success("⛓️ Blockchain Verified")
        
        # Actions
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "📥 Download",
                data=get_certificate_pdf(cert['certificate_id']),
                file_name=f"{cert['certificate_id']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        with col2:
            if st.button("🔗 Share", key=cert['certificate_id'], use_container_width=True):
                show_share_modal(cert)
```

**Features**:
- Certificate gallery
- Download PDF
- Share to LinkedIn
- Blockchain verification badge (Advanced)
- Verification links

---

### 7. Settings (`pages/7_⚙️_Settings.py`)

**Purpose**: User settings and account management

**Layout**:

```python
import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ Settings")

tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "💳 Subscription", "🔔 Notifications", "♿ Accessibility"])

with tab1:
    st.subheader("Profile Information")
    
    email = st.text_input("Email", value=st.session_state['email'], disabled=True)
    user_id = st.text_input("User ID", value=st.session_state['user_id'], disabled=True)
    
    st.caption("Profile information is managed by your license key and cannot be edited here.")

with tab2:
    st.subheader("Subscription & Tier")
    
    tier = st.session_state['tier']
    
    # Current tier card
    st.info(f"**Current Tier:** {tier.title()}")
    
    # Upgrade options
    if tier != 'advanced':
        st.markdown("---")
        st.subheader("🚀 Upgrade Your Tier")
        
        if tier == 'basic':
            col1, col2 = st.columns(2)
            
            with col1:
                render_tier_card('intermediate')
            
            with col2:
                render_tier_card('advanced')
        
        elif tier == 'intermediate':
            render_tier_card('advanced')

with tab3:
    st.subheader("Notification Preferences")
    
    email_notifications = st.checkbox("Email notifications", value=True)
    course_updates = st.checkbox("Course content updates", value=True)
    certificate_alerts = st.checkbox("Certificate earned alerts", value=True)
    
    if st.button("💾 Save Preferences"):
        save_notification_preferences()
        st.success("✅ Preferences saved!")

with tab4:
    st.subheader("Accessibility Settings")
    
    high_contrast = st.checkbox("High contrast mode")
    large_text = st.checkbox("Large text")
    dyslexia_font = st.checkbox("Dyslexia-friendly font (OpenDyslexic)")
    
    if st.button("💾 Save Accessibility Settings"):
        save_accessibility_settings()
        st.success("✅ Settings saved!")
```

**Features**:
- Profile info display
- Tier management and upgrade
- Notification preferences
- Accessibility settings
- License management

---

## UI Components Library

### Reusable Components

**1. Course Card**
```python
def course_card(course: dict):
    with st.container():
        st.image(course['thumbnail'])
        st.markdown(f"**{course['title']}**")
        st.caption(f"{course['duration']}h • {course['difficulty']}")
        st.progress(course['progress'] / 100)
```

**2. Progress Bar with Label**
```python
def labeled_progress(label: str, value: float, max_value: float = 100):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(value / max_value)
    with col2:
        st.caption(f"{value:.0f}%")
```

**3. Stat Card**
```python
def stat_card(label: str, value: str, delta: str = None, icon: str = ""):
    st.metric(f"{icon} {label}", value, delta=delta)
```

**4. Tier Badge**
```python
def tier_badge(tier: str):
    colors = {
        'basic': 'blue',
        'intermediate': 'orange',
        'advanced': 'green'
    }
    st.markdown(f":{colors[tier]}[{tier.upper()}]")
```

---

## Responsive Design

### Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Streamlit Responsive Behavior

```python
# Detect viewport width (approximate)
# Streamlit automatically adjusts columns on mobile

# Desktop: 4 columns
if st.session_state.get('viewport') == 'desktop':
    cols = st.columns(4)
# Tablet: 2 columns
elif st.session_state.get('viewport') == 'tablet':
    cols = st.columns(2)
# Mobile: 1 column
else:
    cols = [st.container()]
```

---

## Theme Configuration

**`.streamlit/config.toml`**:

```toml
[theme]
primaryColor = "#4A90E2"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F7FA"
textColor = "#2C3E50"
font = "sans serif"

[server]
enableXsrfProtection = true
enableCORS = false
```

---

## Navigation Patterns

### Page Transitions

- Use `st.switch_page()` for navigation
- Maintain session state across pages
- Breadcrumb navigation where appropriate

### Back Navigation

```python
if st.button("← Back to Courses"):
    st.switch_page("pages/2_📚_My_Courses.py")
```

---

## Loading States

```python
with st.spinner("Loading course content..."):
    data = fetch_course_data()
    
st.success("✅ Content loaded!")
```

---

## Error States

```python
try:
    result = risky_operation()
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")
    st.info("💡 Try refreshing the page or contact support.")
```

---

## Empty States

```python
if not courses:
    st.info("📚 No courses available yet. Check back soon!")
```

---

## Conclusion

CoursePlayerApp's UI/UX design prioritizes clarity, accessibility, and progressive disclosure of features based on tier. The Streamlit framework enables rapid development while maintaining a professional, cohesive user experience.

