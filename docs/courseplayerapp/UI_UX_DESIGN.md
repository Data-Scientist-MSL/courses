# CoursePlayerApp UI/UX Design Specification

## Design Principles

### Core Principles

1. **Distraction-Free Learning**: Minimize cognitive load with clean, focused interfaces
2. **Mobile-First Responsive**: Seamless experience across desktop, tablet, and mobile
3. **Accessibility First**: WCAG 2.1 AA compliant by design
4. **Fast & Performant**: Page loads <2 seconds, smooth interactions
5. **Consistent & Intuitive**: Predictable patterns, clear navigation
6. **Progressive Disclosure**: Show advanced features as needed, keep basics simple

---

## Visual Design System

### Color Palette

```css
/* Primary Colors */
--primary-blue: #4a90e2;      /* CTAs, links, active states */
--primary-dark: #2c5aa0;      /* Hover states, headers */
--primary-light: #e3f2fd;     /* Backgrounds, highlights */

/* Secondary Colors */
--secondary-teal: #26a69a;    /* Success states, completed items */
--secondary-purple: #7b1fa2;  /* Premium/Advanced tier features */
--secondary-gold: #ffd700;    /* Achievements, badges */

/* Neutral Colors */
--neutral-900: #1a1a1a;       /* Primary text */
--neutral-700: #4a4a4a;       /* Secondary text */
--neutral-500: #9e9e9e;       /* Disabled text */
--neutral-300: #e0e0e0;       /* Borders */
--neutral-100: #f5f5f5;       /* Backgrounds */
--neutral-white: #ffffff;     /* Card backgrounds */

/* Semantic Colors */
--success: #4caf50;           /* Completed, passed */
--warning: #ff9800;           /* Warnings, quota low */
--error: #f44336;             /* Errors, failed */
--info: #2196f3;              /* Info messages */

/* Tier Colors */
--tier-basic: #90a4ae;        /* Basic tier badge */
--tier-intermediate: #26a69a; /* Intermediate tier badge */
--tier-advanced: #7b1fa2;     /* Advanced tier badge */
```

### Typography

```css
/* Font Families */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-heading: 'Poppins', sans-serif;
--font-mono: 'Fira Code', 'Courier New', monospace;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px - Captions */
--text-sm: 0.875rem;   /* 14px - Small text */
--text-base: 1rem;     /* 16px - Body text */
--text-lg: 1.125rem;   /* 18px - Large body */
--text-xl: 1.25rem;    /* 20px - Small headings */
--text-2xl: 1.5rem;    /* 24px - Section headings */
--text-3xl: 1.875rem;  /* 30px - Page headings */
--text-4xl: 2.25rem;   /* 36px - Hero text */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### Spacing System

```css
/* 8px base unit */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

### Border Radius

```css
--radius-sm: 4px;    /* Small elements (buttons, inputs) */
--radius-md: 8px;    /* Cards, containers */
--radius-lg: 12px;   /* Large cards, modals */
--radius-xl: 16px;   /* Hero sections */
--radius-full: 9999px; /* Pills, avatars */
```

### Shadows

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

---

## Page Layouts

### 1. Dashboard/Home Page

**Purpose**: Central hub for course navigation and progress overview

**Layout Structure**:
```
┌─────────────────────────────────────────────────────────┐
│ Header: Logo | Search | Notifications | Profile         │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Hero Section: "Welcome back, [Name]!"              │ │
│ │ Continue Learning: Resume [Course] at [Progress]   │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                           │
│ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌──────────┐ │
│ │ Progress  │ │ Streak    │ │ Certificates│ │ AI Tutor│ │
│ │   73%     │ │  🔥 7d    │ │     3      │ │ 23/50 Q │ │
│ └───────────┘ └───────────┘ └───────────┘ └──────────┘ │
│                                                           │
│ My Courses:                                              │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
│ │ Course 1 │ │ Course 2 │ │ Course 3 │                 │
│ │ [Image]  │ │ [Image]  │ │ [Image]  │                 │
│ │ 73% done │ │ 45% done │ │ Not start│                 │
│ └──────────┘ └──────────┘ └──────────┘                 │
│                                                           │
│ Recommended Courses:                                     │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
│ │ Course A │ │ Course B │ │ Course C │                 │
│ └──────────┘ └──────────┘ └──────────┘                 │
└─────────────────────────────────────────────────────────┘
```

**Streamlit Implementation**:
```python
# courseplayerapp/ui/pages/dashboard.py

import streamlit as st

def render_dashboard():
    """Render main dashboard page."""
    
    st.set_page_config(
        page_title="Dashboard - EdGuide",
        page_icon="🎓",
        layout="wide"
    )
    
    # Header
    render_header()
    
    # Hero section with continue learning
    st.title(f"Welcome back, {st.session_state.user_name}! 👋")
    
    if st.session_state.last_viewed_course:
        with st.container():
            st.subheader("Continue Learning")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📚 {st.session_state.last_viewed_course['title']}")
                st.progress(st.session_state.last_viewed_course['progress'] / 100)
                st.caption(f"{st.session_state.last_viewed_course['progress']}% complete")
            with col2:
                if st.button("Resume →", type="primary", use_container_width=True):
                    navigate_to_course(st.session_state.last_viewed_course['id'])
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Progress", "73%", "+5% this week")
    
    with col2:
        streak = get_current_streak(st.session_state.user_id)
        st.metric("Current Streak", f"🔥 {streak} days", f"Record: {get_longest_streak()}")
    
    with col3:
        cert_count = get_certificate_count(st.session_state.user_id)
        st.metric("Certificates Earned", cert_count)
    
    with col4:
        if st.session_state.user_tier in ["intermediate", "advanced"]:
            quota = get_ai_quota_remaining(st.session_state.user_id)
            if st.session_state.user_tier == "advanced":
                st.metric("AI Tutor", "∞ Unlimited")
            else:
                st.metric("AI Tutor", f"{quota}/50 Q")
        else:
            st.metric("AI Tutor", "🔒 Locked")
    
    # Enrolled courses
    st.subheader("My Courses")
    courses = get_user_courses(st.session_state.user_id)
    
    cols = st.columns(3)
    for idx, course in enumerate(courses):
        with cols[idx % 3]:
            render_course_card(course)
    
    # Recommended courses
    st.subheader("Recommended for You")
    recommendations = get_course_recommendations(st.session_state.user_id)
    
    cols = st.columns(3)
    for idx, course in enumerate(recommendations[:3]):
        with cols[idx]:
            render_course_card(course, recommended=True)
```

---

### 2. Course Page

**Purpose**: Main learning interface with curriculum, content, and AI Tutor

**Layout Structure**:
```
┌───────────────────────────────────────────────────────────────┐
│ Header: Logo | Course Title | Progress: 73% | Profile         │
├─────────┬─────────────────────────────────────────────┬───────┤
│ Sidebar │ Main Content Area                           │ AI    │
│         │                                             │ Tutor │
│ ▾ Intro │ ┌─────────────────────────────────────────┐ │       │
│ □ Mod 1 │ │                                         │ │ 💬    │
│ □ Mod 2 │ │      Video Player                       │ │       │
│ ☑ Mod 3 │ │                                         │ │ Ask   │
│   ☑ 3.1 │ └─────────────────────────────────────────┘ │ me... │
│   ☑ 3.2 │                                             │       │
│   ▸ 3.3 │ 🎥 Introduction to Neural Networks         │ Chat  │
│   □ 3.4 │ Duration: 15:30 | Progress: 5:23           │ hist. │
│ □ Mod 4 │                                             │       │
│         │ ⬇️ Download (720p) | 📄 Transcript         │       │
│ 📝 Quiz │                                             │       │
│ 🎓 Cert │ ← Previous | Next →                         │       │
│         │                                             │       │
└─────────┴─────────────────────────────────────────────┴───────┘
```

**Streamlit Implementation**:
```python
# courseplayerapp/ui/pages/course_page.py

def render_course_page(course_id: str):
    """Render course learning page with sidebar curriculum."""
    
    st.set_page_config(layout="wide", page_title=f"{course.title} - EdGuide")
    
    # Course header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title(course.title)
    with col2:
        progress = get_course_progress(st.session_state.user_id, course_id)
        st.metric("Progress", f"{progress}%")
    with col3:
        st.write("")  # Spacer
        if st.button("👤 View Profile"):
            navigate_to_profile()
    
    # Layout: Sidebar + Main + AI Tutor
    sidebar_col, main_col, tutor_col = st.columns([1, 3, 1])
    
    # Curriculum sidebar
    with sidebar_col:
        render_curriculum_sidebar(course)
    
    # Main content area
    with main_col:
        current_resource = st.session_state.get("current_resource")
        
        if current_resource["type"] == "video":
            render_video_player(
                video_id=current_resource["id"],
                user_tier=st.session_state.user_tier
            )
        elif current_resource["type"] == "lab":
            render_lab_runner(
                lab_id=current_resource["id"],
                user_tier=st.session_state.user_tier
            )
        elif current_resource["type"] == "quiz":
            render_quiz(
                quiz_id=current_resource["id"]
            )
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Previous"):
                navigate_to_previous_resource()
        with col3:
            if st.button("Next →", type="primary"):
                navigate_to_next_resource()
    
    # AI Tutor sidebar
    with tutor_col:
        if can_access_feature(st.session_state.user_tier, "ai_tutor_limited") or \
           can_access_feature(st.session_state.user_tier, "ai_tutor_unlimited"):
            render_ai_tutor_chat(st.session_state.user_tier)
        else:
            render_ai_tutor_locked()


def render_curriculum_sidebar(course):
    """Render collapsible curriculum with module/lesson navigation."""
    
    st.sidebar.title("📚 Course Curriculum")
    
    for module in course.modules:
        # Module header (collapsible)
        is_expanded = st.sidebar.checkbox(
            f"{'☑' if module.completed else '□'} {module.title}",
            value=(module.id == st.session_state.current_module),
            key=f"module_{module.id}"
        )
        
        if is_expanded:
            # Show lessons in module
            for lesson in module.lessons:
                icon = "☑" if lesson.completed else "▸"
                if st.sidebar.button(
                    f"  {icon} {lesson.title}",
                    key=f"lesson_{lesson.id}",
                    use_container_width=True
                ):
                    load_lesson(lesson.id)
```

---

### 3. Video Player Page

**Purpose**: Full-screen video watching experience

**Features**:
- Large video player (16:9 aspect ratio)
- Playback controls (play, pause, seek, volume, speed, quality, fullscreen)
- Chapter markers on timeline
- Transcript/notes sidebar (toggle)
- Download button (tier-gated)
- Related resources below video

**Implementation**: See VIDEO_PLAYER.md

---

### 4. Lab Environment Page

**Purpose**: Interactive coding environment

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│ Lab: Build a Neural Network                             │
├────────────────────┬────────────────────────────────────┤
│ Instructions       │ Code Editor / Jupyter Notebook     │
│                    │                                     │
│ Step 1:            │ import numpy as np                 │
│ Import libraries   │ import pandas as pd                │
│                    │                                     │
│ Step 2:            │ # Your code here                   │
│ Load dataset       │                                     │
│                    │                                     │
│ 💡 Hint: Use       │ ▶ Run Cell | 💾 Save | 🔄 Reset   │
│ pd.read_csv()      │                                     │
│                    │ Output:                            │
│ ✅ Tests:          │ > Successfully loaded 1000 rows    │
│ □ Test 1           │                                     │
│ □ Test 2           │                                     │
│                    │                                     │
│ Submit Lab →       │                                     │
└────────────────────┴────────────────────────────────────┘
```

**Implementation**: See LAB_RUNNER.md

---

### 5. Achievements & Certificates Page

**Purpose**: Showcase earned achievements and certificates

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│ Your Achievements 🏆                                     │
├─────────────────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│ │   73%   │ │ 🔥 7d   │ │   3     │ │  250    │       │
│ │Progress │ │ Streak  │ │ Certs   │ │ Points  │       │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘       │
│                                                          │
│ Badges Earned:                                          │
│ 🎬 First Steps  💻 Code Warrior  ⚡ Speed Learner      │
│ 🔥 Week Warrior  🏆 Course Champion                    │
│                                                          │
│ Certificates:                                           │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │
│ │ ML Course    │ │ Data Science │ │ Python Basics│    │
│ │ [Preview]    │ │ [Preview]    │ │ [Preview]    │    │
│ │ Jan 2026     │ │ Dec 2025     │ │ Nov 2025     │    │
│ │ Grade: 95%   │ │ Grade: 88%   │ │ Grade: 92%   │    │
│ │ 📄 📱 🔗     │ │ 📄 📱 🔗     │ │ 📄 📱 🔗     │    │
│ └──────────────┘ └──────────────┘ └──────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**Implementation**: See CERTIFICATE_DISPLAY.md

---

## Dark Mode & Light Mode

### Theme Toggle

```python
# courseplayerapp/ui/components/theme_toggle.py

def render_theme_toggle():
    """Render theme toggle switch."""
    
    current_theme = st.session_state.get("theme", "light")
    
    if st.sidebar.toggle("🌙 Dark Mode", value=(current_theme == "dark")):
        st.session_state.theme = "dark"
        apply_dark_theme()
    else:
        st.session_state.theme = "light"
        apply_light_theme()

def apply_dark_theme():
    """Apply dark mode styles."""
    st.markdown("""
        <style>
        :root {
            --background: #1a1a1a;
            --surface: #2d2d2d;
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
        }
        </style>
    """, unsafe_allow_html=True)

def apply_light_theme():
    """Apply light mode styles."""
    st.markdown("""
        <style>
        :root {
            --background: #ffffff;
            --surface: #f5f5f5;
            --text-primary: #1a1a1a;
            --text-secondary: #4a4a4a;
        }
        </style>
    """, unsafe_allow_html=True)
```

---

## Responsive Design

### Breakpoints

```css
/* Mobile */
@media (max-width: 640px) {
    /* Single column layout */
    /* Collapsible sidebar */
    /* Larger touch targets (44px min) */
}

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) {
    /* Two column layout */
    /* Sidebar overlay */
}

/* Desktop */
@media (min-width: 1025px) {
    /* Three column layout (sidebar + main + AI tutor) */
    /* Fixed sidebar */
}
```

### Mobile Optimizations

1. **Navigation**: Bottom tab bar on mobile
2. **Video Player**: Full-width on mobile, landscape optimization
3. **AI Tutor**: Modal/bottom sheet instead of sidebar
4. **Touch Targets**: Minimum 44x44px for buttons
5. **Font Sizes**: Slightly larger on mobile (16px minimum)

---

## Loading States & Feedback

### Skeleton Screens

```python
def render_loading_skeleton():
    """Show skeleton screen while content loads."""
    
    # Placeholder boxes
    st.markdown("""
        <div class="skeleton-box" style="width: 100%; height: 400px;"></div>
        <div class="skeleton-text" style="width: 60%; height: 20px; margin: 10px 0;"></div>
        <div class="skeleton-text" style="width: 80%; height: 20px;"></div>
    """, unsafe_allow_html=True)
```

### Progress Indicators

```python
# Long-running operations
with st.spinner("Loading course content..."):
    course_data = fetch_course_data()

# Upload progress
st.progress(upload_percent / 100, text=f"Uploading: {upload_percent}%")
```

### Toast Notifications

```python
# Success
st.success("✅ Lab submitted successfully!")

# Error
st.error("❌ Failed to save progress. Please try again.")

# Warning
st.warning("⚠️ Only 5 AI Tutor questions remaining this month")

# Info
st.info("💡 Tip: Use keyboard shortcuts to navigate faster")
```

---

## Accessibility Features

### Focus States

```css
/* Visible focus indicators */
button:focus, a:focus, input:focus {
    outline: 2px solid var(--primary-blue);
    outline-offset: 2px;
}
```

### Skip Links

```html
<!-- Allow keyboard users to skip to main content -->
<a href="#main-content" class="skip-link">Skip to main content</a>
```

### ARIA Labels

```python
st.button("▶", aria_label="Play video")
st.text_input("", placeholder="Search courses...", aria_label="Search courses")
```

**See ACCESSIBILITY.md for complete specification**

---

## Performance Optimization

### Code Splitting

- Load video player component only when needed
- Lazy load AI Tutor chat interface
- Defer loading of non-critical assets

### Image Optimization

```python
# Use WebP format with fallback
# Responsive images with srcset
# Lazy loading for below-the-fold images

<img 
    src="course-thumbnail.webp" 
    srcset="course-thumbnail-320.webp 320w, course-thumbnail-640.webp 640w"
    loading="lazy"
    alt="Machine Learning Fundamentals course thumbnail"
/>
```

### Caching

```python
# Cache expensive computations
@st.cache_data(ttl=3600)
def get_course_data(course_id: str):
    return fetch_from_database(course_id)

# Cache API calls
@st.cache_resource
def get_api_client():
    return HTTPClient()
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-14  
**Author**: EdGuide Design Team  
**Platform**: EdGuide (gai-observe.online)
