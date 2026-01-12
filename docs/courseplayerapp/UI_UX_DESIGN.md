# UI/UX Design Specification

## Platform Information
- **Platform**: EdGuide
- **Domain**: gai-observe.online
- **Purpose**: Define user interface and experience design for CoursePlayerApp

---

## Design Principles

### Core Principles

1. **Clean & Distraction-Free Learning**
   - Minimize UI clutter during video playback
   - Focus on content, not chrome
   - Progressive disclosure of features

2. **Mobile-First, Responsive Design**
   - Desktop: Full-featured experience
   - Tablet: Optimized touch interface
   - Mobile: Essential features, streamlined

3. **Fast & Performant**
   - Page load < 2 seconds
   - Video start < 3 seconds
   - Smooth 60fps animations
   - Optimized images (WebP, lazy loading)

4. **Accessible by Default**
   - WCAG 2.1 AA compliance
   - Keyboard navigation
   - Screen reader support
   - High contrast mode

5. **Consistent & Intuitive**
   - Predictable navigation
   - Familiar patterns
   - Clear visual hierarchy
   - Consistent spacing/typography

---

## Design System

### Color Palette

```yaml
colors:
  # Primary colors
  primary:
    main: "#2C3E50"       # Dark blue-gray
    light: "#34495E"
    dark: "#1A252F"
    
  # Accent colors
  accent:
    main: "#3498DB"       # Blue
    light: "#5DADE2"
    dark: "#2874A6"
    
  # Semantic colors
  success: "#27AE60"      # Green
  warning: "#F39C12"      # Orange
  error: "#E74C3C"        # Red
  info: "#3498DB"         # Blue
  
  # Tier colors (for badges)
  basic: "#95A5A6"        # Gray
  intermediate: "#3498DB" # Blue
  advanced: "#F39C12"     # Gold
  
  # Neutral colors
  neutral:
    100: "#F8F9FA"        # Lightest
    200: "#E9ECEF"
    300: "#DEE2E6"
    400: "#CED4DA"
    500: "#ADB5BD"
    600: "#6C757D"
    700: "#495057"
    800: "#343A40"
    900: "#212529"        # Darkest
  
  # Background
  background:
    light: "#FFFFFF"
    dark: "#1A1A1A"
    
  # Text
  text:
    primary: "#212529"
    secondary: "#6C757D"
    disabled: "#ADB5BD"
    inverse: "#FFFFFF"
```

### Typography

```yaml
typography:
  font_families:
    sans: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    serif: "'Merriweather', Georgia, serif"
    mono: "'JetBrains Mono', 'Fira Code', monospace"
  
  font_sizes:
    xs: "0.75rem"    # 12px
    sm: "0.875rem"   # 14px
    base: "1rem"     # 16px
    lg: "1.125rem"   # 18px
    xl: "1.25rem"    # 20px
    "2xl": "1.5rem"  # 24px
    "3xl": "1.875rem"# 30px
    "4xl": "2.25rem" # 36px
    "5xl": "3rem"    # 48px
  
  font_weights:
    light: 300
    normal: 400
    medium: 500
    semibold: 600
    bold: 700
    extrabold: 800
  
  line_heights:
    tight: 1.25
    normal: 1.5
    relaxed: 1.75
    loose: 2
```

### Spacing System

```yaml
spacing:
  # Base unit: 0.25rem (4px)
  0: "0"
  1: "0.25rem"   # 4px
  2: "0.5rem"    # 8px
  3: "0.75rem"   # 12px
  4: "1rem"      # 16px
  5: "1.25rem"   # 20px
  6: "1.5rem"    # 24px
  8: "2rem"      # 32px
  10: "2.5rem"   # 40px
  12: "3rem"     # 48px
  16: "4rem"     # 64px
  20: "5rem"     # 80px
  24: "6rem"     # 96px
```

### Component Library

```yaml
components:
  buttons:
    primary:
      bg: "accent.main"
      text: "text.inverse"
      hover_bg: "accent.dark"
      
    secondary:
      bg: "transparent"
      text: "accent.main"
      border: "accent.main"
      hover_bg: "accent.light"
      
    danger:
      bg: "error"
      text: "text.inverse"
      
  cards:
    bg: "background.light"
    border: "neutral.300"
    shadow: "0 2px 4px rgba(0,0,0,0.1)"
    hover_shadow: "0 4px 8px rgba(0,0,0,0.15)"
    
  inputs:
    border: "neutral.400"
    focus_border: "accent.main"
    placeholder: "text.secondary"
```

---

## Page Layouts

### 1. Dashboard / Home Page

**Purpose**: Course overview, resume learning, progress summary

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  [Logo]  Dashboard  My Courses  Achievements  [Profile] │ ← Header
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Welcome back, John! 🎉              [Tier Badge: 🥈]  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Continue Learning                               │   │
│  │ ┌──────────────┐  Machine Learning              │   │
│  │ │  [Thumbnail] │  Module 3: Neural Networks     │   │
│  │ │     Video    │  ▓▓▓▓▓▓▓▓▓░░░ 75% Complete     │   │
│  │ └──────────────┘  [Continue →]                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────┬─────────┬─────────┬─────────┐             │
│  │ Course  │ Current │ Study   │ Points  │             │
│  │ Progress│ Streak  │ Time    │ Earned  │             │
│  │  67%    │ 🔥 12   │ 28 hrs  │  450    │             │
│  └─────────┴─────────┴─────────┴─────────┘             │
│                                                         │
│  My Courses                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │ [Thumbnail] │ │ [Thumbnail] │ │ [Thumbnail] │       │
│  │ Machine     │ │ Data Science│ │ Deep        │       │
│  │ Learning    │ │ Basics      │ │ Learning    │       │
│  │ ▓▓▓▓▓▓░░░   │ │ ▓▓▓▓▓▓▓▓▓▓  │ │ ▓░░░░░░░░░  │       │
│  │ 67%         │ │ 100% ✓      │ │ 5%          │       │
│  │ [Open]      │ │ [Review]    │ │ [Start]     │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Streamlit Implementation**:
```python
def render_dashboard(user_id, user_tier):
    st.set_page_config(page_title="Dashboard - EdGuide", layout="wide")
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title(f"Welcome back, {get_user_name(user_id)}! 🎉")
    with col3:
        render_tier_badge(user_tier)
    
    # Continue Learning Card
    st.markdown("### Continue Learning")
    resume = get_resume_learning(user_id)
    
    if resume:
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.image(resume["thumbnail"], use_column_width=True)
        with col_b:
            st.subheader(resume["course_title"])
            st.caption(resume["current_module"])
            st.progress(resume["completion"] / 100)
            st.button("Continue →", type="primary")
    
    # Metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = get_user_metrics(user_id)
    
    with col1:
        st.metric("Course Progress", f"{metrics['progress']}%")
    with col2:
        st.metric("Current Streak", f"🔥 {metrics['streak']}")
    with col3:
        st.metric("Study Time", f"{metrics['hours']} hrs")
    with col4:
        st.metric("Points Earned", metrics['points'])
    
    # Course Grid
    st.markdown("---")
    st.markdown("### My Courses")
    
    courses = get_user_courses(user_id)
    cols = st.columns(3)
    
    for idx, course in enumerate(courses):
        col = cols[idx % 3]
        with col:
            render_course_card(course)
```

### 2. Course Page

**Purpose**: Course curriculum, main learning interface

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  [Logo]  Machine Learning Fundamentals    [🥈 Pro]      │
├────┬────────────────────────────────────────────────────┤
│ 📋 │                                                    │
│Cur │  Module 3: Neural Networks                        │
│ric │  Lesson 2: Backpropagation                        │
│ulu │                                                    │
│ m  │  ┌──────────────────────────────────────────┐     │
│    │  │                                          │     │
│ ✅ │  │         Video Player                     │     │
│Mod │  │        [▶ Play Button]                   │     │
│ 1  │  │                                          │     │
│    │  │  00:05:32 / 00:15:00  ▓▓▓▓▓░░░░░░       │     │
│ ✅ │  └──────────────────────────────────────────┘     │
│Mod │                                                    │
│ 2  │  [⬇️ Download] [🔖 Bookmark] [📝 Notes]           │
│    │                                                    │
│ ⏳ │  ┌────────────────────────────────────┐           │
│Mod │  │ 🤖 AI Tutor                        │           │
│ 3  │  │ Ask me anything about this lesson  │           │
│ │  │  │ Questions: 23/50 remaining         │           │
│ └┐ │  │ [Ask Question]                     │           │
│  ◉ │  └────────────────────────────────────┘           │
│  │ │                                                    │
│  └ │                                                    │
│    │                                                    │
└────┴────────────────────────────────────────────────────┘
```

**Features**:
- **Collapsible Sidebar**: Course curriculum with progress indicators
- **Main Content Area**: Video/Lab/Quiz display
- **AI Tutor Panel**: Collapsible chat interface (right side or bottom)
- **Quick Actions**: Download, bookmark, notes

### 3. Video Player Page (Fullscreen Mode)

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                                                         │
│                                                         │
│                 Video Player                            │
│               (16:9 aspect ratio)                       │
│                                                         │
│                                                         │
│                                                         │
│ ═══════════════════════════════════════════════════════ │ ← Timeline
│ [▶] 00:05:32 / 00:15:00  [🔊] [CC] [⚙️] [⛶]            │ ← Controls
├─────────────────────────────────────────────────────────┤
│  📑 Chapters         📝 Transcript         💬 Discussion│ ← Tabs
│                                                         │
│  00:00 - Introduction                                   │
│  02:15 - Key Concepts                                   │
│  05:30 - Example Code ← (current)                       │
│  10:00 - Practice Problem                               │
│  14:00 - Summary                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4. Lab Environment Page

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  Lab 3.1: Implementing a Neural Network                │
├──────────────────┬──────────────────────────────────────┤
│ 📋 Instructions  │  💻 Code Editor / 📓 Notebook         │
│                  │                                       │
│ Step 1: Import   │  ```python                            │
│ libraries        │  import numpy as np                   │
│                  │  import pandas as pd                  │
│ Step 2: Load     │  ```                                  │
│ data             │                                       │
│                  │  [▶ Run] [💾 Save] [🔄 Reset]         │
│ Step 3: Build    │                                       │
│ model            │  ───────────────────────────────────  │
│                  │  Output:                              │
│ 💡 Hints         │  > Successfully imported libraries    │
│ [Show Hint 1]    │  > Data shape: (1000, 10)             │
│ [Show Hint 2]    │                                       │
│                  │  ⌨️ Terminal                          │
│ ✅ Validation    │  $ pip install matplotlib             │
│ [Check Solution] │  $                                    │
│                  │                                       │
└──────────────────┴──────────────────────────────────────┘
```

**Features**:
- **Split View**: Instructions (left) + Code/Terminal (right)
- **Resizable Panels**: User can adjust split ratio
- **Tabs**: Switch between Code Editor, Notebook, Terminal
- **Progress Indicators**: Visual feedback on completion

### 5. Achievements / Certificates Page

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  🏆 Your Achievements                                   │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┬─────────┬─────────┐                        │
│  │ Earned  │Progress │  Points │                        │
│  │   12    │    5    │   450   │                        │
│  └─────────┴─────────┴─────────┘                        │
│                                                         │
│  [All] [Earned] [In Progress] [Streak] [Milestone]     │
│                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │ ✅          │ │ ⏳          │ │ ✅          │       │
│  │ 🔥          │ │ 📚          │ │ 💯          │       │
│  │ Week Warrior│ │ Binge       │ │ Perfect     │       │
│  │             │ │ Learner     │ │ Score       │       │
│  │ Study 7 days│ │ Watch 50    │ │ 100% on quiz│       │
│  │ in a row    │ │ videos      │ │             │       │
│  │ 25 pts ⭐   │ │ 45/50 ▓▓▓░░ │ │ 30 pts ⭐   │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
│                                                         │
│  🎓 Your Certificates                                   │
│                                                         │
│  ┌────────────────┐ ┌────────────────┐                 │
│  │ [Certificate]  │ │ [Certificate]  │                 │
│  │ Machine        │ │ Data Science   │                 │
│  │ Learning       │ │ Basics         │                 │
│  │ Jan 12, 2026   │ │ Dec 5, 2025    │                 │
│  │ Grade: 92%     │ │ Grade: 88%     │                 │
│  │ [View][Share]  │ │ [View][Share]  │                 │
│  └────────────────┘ └────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

---

## Mobile Responsive Design

### Breakpoints

```yaml
breakpoints:
  mobile: "< 640px"
  tablet: "640px - 1024px"
  desktop: "> 1024px"
```

### Mobile Adaptations

**Dashboard (Mobile)**:
- Single column layout
- Stacked metrics
- Hamburger menu for navigation
- Bottom navigation bar (Home, Courses, Progress, Profile)

**Course Page (Mobile)**:
- Collapsible sidebar (drawer)
- Full-width video player
- Tabs for content (Video, Notes, AI Tutor)
- Floating action button for quick actions

**Video Player (Mobile)**:
- Portrait mode support
- Touch gestures (double-tap to skip, swipe for volume/brightness)
- Mobile-optimized controls
- Picture-in-picture for multitasking

---

## Dark Mode Support

### Color Scheme Toggle

```python
def render_theme_toggle():
    """Toggle between light and dark mode"""
    
    theme = st.session_state.get("theme", "light")
    
    if st.button("🌓 Toggle Theme"):
        new_theme = "dark" if theme == "light" else "light"
        st.session_state.theme = new_theme
        apply_theme(new_theme)
        st.rerun()
```

### Dark Mode Colors

```yaml
dark_mode:
  background:
    primary: "#1A1A1A"
    secondary: "#2D2D2D"
    tertiary: "#3A3A3A"
    
  text:
    primary: "#FFFFFF"
    secondary: "#B0B0B0"
    disabled: "#6C6C6C"
    
  accent:
    main: "#5DADE2"  # Lighter blue for dark backgrounds
```

---

## Animation & Transitions

### Animation Principles

```yaml
animations:
  duration:
    instant: "0ms"
    fast: "150ms"
    normal: "300ms"
    slow: "500ms"
    
  easing:
    ease_in: "cubic-bezier(0.4, 0, 1, 1)"
    ease_out: "cubic-bezier(0, 0, 0.2, 1)"
    ease_in_out: "cubic-bezier(0.4, 0, 0.2, 1)"
    
  use_cases:
    hover: "150ms ease-out"
    page_transition: "300ms ease-in-out"
    modal: "300ms ease-out"
    drawer: "300ms ease-in-out"
```

### Key Animations

1. **Page Transitions**: Fade in (300ms)
2. **Button Hover**: Scale up slightly (150ms)
3. **Card Hover**: Lift shadow (200ms)
4. **Loading States**: Skeleton screens, spinners
5. **Success/Error**: Slide in from top (300ms)

---

## Iconography

### Icon Library

**Primary**: Heroicons (https://heroicons.com)
**Alternative**: Lucide Icons (https://lucide.dev)

**Common Icons**:
```yaml
icons:
  navigation:
    home: "home"
    courses: "academic-cap"
    progress: "chart-bar"
    achievements: "trophy"
    profile: "user-circle"
    
  actions:
    play: "play"
    pause: "pause"
    download: "arrow-down-tray"
    share: "share"
    bookmark: "bookmark"
    settings: "cog"
    
  status:
    completed: "check-circle"
    in_progress: "clock"
    locked: "lock-closed"
    
  tier:
    basic: "shield"
    intermediate: "shield-check"
    advanced: "shield-exclamation"
```

---

## Loading States

### Skeleton Screens

```python
def render_loading_skeleton():
    """Show skeleton while content loads"""
    
    # Course card skeleton
    with st.container():
        st.markdown("""
        <div class="skeleton skeleton-image"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text short"></div>
        """, unsafe_allow_html=True)
```

### Progress Indicators

1. **Determinate Progress Bar**: For file uploads, video buffering
2. **Indeterminate Spinner**: For API calls
3. **Skeleton Screens**: For page loads
4. **Shimmer Effect**: For image loading

---

## Error States

### Error Handling UI

```python
def render_error_state(error_type: str, message: str):
    """Display user-friendly error messages"""
    
    if error_type == "network":
        st.error("🌐 Connection Error")
        st.write("Please check your internet connection and try again.")
        st.button("🔄 Retry")
        
    elif error_type == "permission":
        st.warning("🔒 Access Denied")
        st.write(message)
        st.button("⬆️ Upgrade Plan")
        
    elif error_type == "not_found":
        st.info("🔍 Content Not Found")
        st.write("This resource doesn't exist or has been moved.")
        st.button("🏠 Go Home")
```

---

## Accessibility Features

### Keyboard Navigation

```yaml
keyboard_shortcuts:
  global:
    "/": "Search"
    "g + h": "Go to Home"
    "g + c": "Go to Courses"
    "g + p": "Go to Progress"
    "?": "Show keyboard shortcuts"
    
  video_player:
    "space": "Play/Pause"
    "←/→": "Seek ±10s"
    "↑/↓": "Volume ±10%"
    "m": "Mute"
    "f": "Fullscreen"
    "c": "Toggle captions"
```

### Focus Management

- Clear focus indicators (2px outline)
- Skip to main content link
- Logical tab order
- Focus trap in modals
- Return focus after modal close

---

## Performance Optimization

### Best Practices

1. **Image Optimization**
   - WebP format with fallback
   - Responsive images (`srcset`)
   - Lazy loading for below-fold images
   - Blur-up placeholders

2. **Code Splitting**
   - Route-based code splitting
   - Dynamic imports for heavy components
   - Separate vendor bundles

3. **Caching Strategy**
   - Service worker for offline support
   - CDN for static assets
   - API response caching
   - Browser caching headers

4. **Bundle Optimization**
   - Tree shaking
   - Minification
   - Compression (gzip/brotli)
   - Critical CSS inlining

---

## Related Documentation

- [System Architecture](./ARCHITECTURE.md)
- [Feature Gating](./FEATURE_GATING.md)
- [Video Player](./VIDEO_PLAYER.md)
- [Accessibility](./ACCESSIBILITY.md)

---

**Last Updated**: January 2026  
**Platform**: EdGuide (gai-observe.online)  
**Version**: 1.0
