# CoursePlayerApp - UI/UX Specifications

## Overview

This document specifies the user interface and user experience design for CoursePlayerApp's Streamlit-based interface. It includes page layouts, component specifications, tier-based variations, and UX patterns.

## Design Philosophy

CoursePlayerApp follows these UX principles:

1. **Progressive Disclosure**: Show basic features first, reveal advanced features as needed
2. **Tier Transparency**: Clear indication of user's tier and available features
3. **Non-Intrusive Upgrades**: Upgrade prompts that inform without annoying
4. **Consistent Patterns**: Reusable UI patterns across all pages
5. **Accessibility**: WCAG 2.1 AA compliance
6. **Performance**: Fast loading, responsive interactions

## Page Structure

```
CoursePlayerApp/
└── pages/
    ├── 00_🏠_Home.py              # Dashboard, recent courses, achievements
    ├── 01_📚_Course_Browser.py    # Browse curriculum, filter by track
    ├── 02_🎓_Learn.py             # Main learning interface
    ├── 03_🧪_Labs.py              # Notebook execution
    ├── 04_🤖_AI_Tutor.py          # Chat interface
    ├── 05_📊_Progress.py          # Completion tracking, analytics
    ├── 06_🏆_Achievements.py      # Badges, rewards, streak
    ├── 07_📜_Certificates.py      # View/download certificates
    ├── 08_💾_Datasets.py          # Dataset explorer
    └── 09_⚙️_Settings.py          # License info, upgrade, preferences
```

## Page Specifications

### 00_🏠_Home.py - Dashboard

**Purpose**: Welcome page showing overview of learning journey and quick access to key features.

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ 🎓 CoursePlayerApp                    [Tier Badge] [Settings]│
├─────────────────────────────────────────────────────────────┤
│ Welcome back, [Name]! 👋                                     │
│                                                               │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │
│ │  📚 Courses  │ │  🔥 Streak   │ │  🏆 Badges   │         │
│ │      5       │ │   14 days    │ │      12      │         │
│ └──────────────┘ └──────────────┘ └──────────────┘         │
│                                                               │
│ Continue Learning                                            │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ [Thumbnail] Data Science 101                         │   │
│ │ Lesson 5: Pandas DataFrames          ████████░░ 80% │   │
│ │ [Continue] [10 min remaining]                        │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                               │
│ Recent Activity                                              │
│ • Completed "Introduction to ML" quiz - 95% ✓               │
│ • Unlocked "Data Wrangler" badge 🏆                         │
│ • Asked AI Tutor 3 questions (47 remaining this month)      │
│                                                               │
│ Recommended for You                                          │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│ │ ML Basics  │ │ Deep Learn │ │ NLP Course │               │
│ └────────────┘ └────────────┘ └────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

**Components Used**:
- Dashboard metrics (courses, streak, badges)
- Course progress card
- Activity feed
- Course recommendations

**Tier Variations**:
- **Basic**: Shows locked features in recommendations
- **Intermediate**: Full feature access, quota indicators
- **Advanced**: Unlimited features, no quota displays

**User Flows**:
1. User lands on dashboard
2. Sees current course progress
3. Clicks "Continue" to resume learning
4. OR browses recommended courses
5. OR checks recent achievements

**Edge Cases**:
- No active courses: Show course browser CTA
- Expired license: Show renewal prompt
- New user: Show onboarding wizard

### 01_📚_Course_Browser.py - Course Browser

**Purpose**: Browse available courses, filter by track, check access requirements.

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ 📚 Course Browser                                            │
├─────────────────────────────────────────────────────────────┤
│ [Search: _____________________] [Filter ▼] [Sort: Popular ▼]│
│                                                               │
│ Filters: ☑ All Levels  ☑ All Tracks                         │
│          ☐ Beginner  ☐ Intermediate  ☐ Advanced             │
│                                                               │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ 📊 Data Science Fundamentals              [Basic ✓]  │   │
│ │ Master the foundations of data science                │   │
│ │ • 8 hours • 12 lessons • 5 quizzes                   │   │
│ │ [Enroll Now] [Preview]                    ⭐⭐⭐⭐⭐ │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                               │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ 🤖 Machine Learning Advanced     🔒 [Intermediate]   │   │
│ │ Deep dive into ML algorithms and techniques           │   │
│ │ • 20 hours • 30 lessons • Interactive labs           │   │
│ │ [Upgrade to Access]                       ⭐⭐⭐⭐⭐ │   │
│ └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Components Used**:
- Search bar
- Filter chips
- Course cards with access badges
- Enrollment/access CTAs

**Tier Variations**:
- **Basic**: Some courses locked with upgrade CTA
- **Intermediate**: More courses unlocked
- **Advanced**: All courses accessible

**User Flows**:
1. User browses courses
2. Filters by track/level
3. Clicks course to see details
4. Enrolls if accessible, or sees upgrade prompt
5. Starts first lesson

### 02_🎓_Learn.py - Learning Interface

**Purpose**: Main interface for consuming course content (videos, slides, lessons).

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ ← Back to Courses | Data Science 101 > Lesson 5             │
├─────────────────────────────────────────────────────────────┤
│ ┌───────────────┐ ┌───────────────────────────────────────┐ │
│ │ 📑 Lessons    │ │                                       │ │
│ │               │ │      Video Player                     │ │
│ │ ✓ 1. Intro    │ │      [════════════════]               │ │
│ │ ✓ 2. Setup    │ │                                       │ │
│ │ ▶ 3. Pandas   │ │      [⏯] [🔊] [⚙] [⬇ Intermediate+]  │ │
│ │ ○ 4. Numpy    │ │                                       │ │
│ │ ○ 5. Viz      │ │ 📊 Slides                             │ │
│ │               │ │ [Slide 1 of 15]         [Download ▼] │ │
│ │ 🏆 Quizzes    │ │ [< Prev]          [Next >]            │ │
│ │ ○ Quiz 1      │ │                                       │ │
│ │ ○ Final       │ │ 📝 Lesson Notes                       │ │
│ │               │ │ Key takeaways from this lesson...     │ │
│ └───────────────┘ └───────────────────────────────────────┘ │
│                                                               │
│ [← Previous Lesson]  [Mark Complete]  [Next Lesson →]        │
└─────────────────────────────────────────────────────────────┘
```

**Components Used**:
- Video Player (with tier-based controls)
- Slides Viewer
- Lesson sidebar navigation
- Progress tracking

**Tier Variations**:
- **Basic**: Streaming only, no downloads
- **Intermediate**: Download buttons, transcripts
- **Advanced**: All features, annotations

**User Flows**:
1. User selects lesson from sidebar
2. Watches video
3. Reviews slides
4. Reads lesson notes
5. Marks lesson complete
6. Proceeds to next lesson

**Edge Cases**:
- Video fails to load: Show error, retry button
- Locked lesson: Show prerequisite requirements
- Quota exceeded: For features like downloads

### 03_🧪_Labs.py - Lab Runner

**Purpose**: Execute Jupyter notebooks with tier-appropriate environment.

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ 🧪 Labs - Data Science 101                                   │
├─────────────────────────────────────────────────────────────┤
│ Lab: Pandas Data Manipulation                                │
│                                                               │
│ ┌─ Basic Tier ─────────────────────────────────────────┐   │
│ │ 📖 View-Only Mode                                     │   │
│ │ This notebook is displayed in read-only mode.         │   │
│ │ Upgrade to Intermediate for interactive execution.    │   │
│ │ [Upgrade] [Learn More]                                │   │
│ │                                                        │   │
│ │ [Notebook HTML Preview]                               │   │
│ └───────────────────────────────────────────────────────┘   │
│                                                               │
│ ┌─ Intermediate Tier ──────────────────────────────────┐   │
│ │ 🌐 JupyterLite (Browser Execution)                    │   │
│ │ [▶ Run All] [⬇ Download] [📝 Reset]                  │   │
│ │                                                        │   │
│ │ [JupyterLite Iframe]                                  │   │
│ └───────────────────────────────────────────────────────┘   │
│                                                               │
│ ┌─ Advanced Tier ──────────────────────────────────────┐   │
│ │ 🚀 JupyterLab (Full Environment)                      │   │
│ │ [Open in JupyterLab] [🎮 GPU Enabled] [⬇ Download]   │   │
│ │ Your work is automatically saved.                     │   │
│ └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Components Used**:
- Lab Runner (tier-specific)
- Upgrade prompts
- Download buttons (gated)

**Tier Variations**:
- **Basic**: Static HTML view only
- **Intermediate**: JupyterLite browser execution
- **Advanced**: Full JupyterLab with GPU

**User Flows**:
1. User selects lab
2. Views notebook (Basic) OR executes (Intermediate+)
3. Downloads completed notebook
4. Submits for code review (if enabled)

### 04_🤖_AI_Tutor.py - AI Tutor Chat

**Purpose**: Chat with OLLAMA-powered AI tutor for course help.

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ 🤖 AI Tutor - Data Science 101                               │
├─────────────────────────────────────────────────────────────┤
│ Questions remaining: 47/50 this month    [Reset: Jan 1]     │
│                                                               │
│ ┌───────────────────────────────────────────────────────┐   │
│ │ 👤 You (2:30 PM)                                      │   │
│ │ What is the difference between a DataFrame and        │   │
│ │ a Series in pandas?                                   │   │
│ │                                                        │   │
│ │ 🤖 AI Tutor (2:30 PM)                                 │   │
│ │ Great question! Based on the course materials:        │   │
│ │                                                        │   │
│ │ A **Series** is a one-dimensional array...            │   │
│ │ A **DataFrame** is a two-dimensional table...         │   │
│ │                                                        │   │
│ │ See Lesson 3, Slide 8 for visual examples.           │   │
│ │                                                        │   │
│ │ 👤 You (2:32 PM)                                      │   │
│ │ Can you show me an example?                           │   │
│ └───────────────────────────────────────────────────────┘   │
│                                                               │
│ [Type your question...                              ] [Send] │
│                                                               │
│ 💡 Tips: Ask about concepts, code errors, or practice        │
│    problems from the current course.                         │
└─────────────────────────────────────────────────────────────┘
```

**Components Used**:
- AI Tutor Chat interface
- Quota indicator
- Context-aware responses

**Tier Variations**:
- **Basic**: Feature locked, upgrade prompt
- **Intermediate**: 50 questions/month, llama3.2:3b
- **Advanced**: Unlimited, llama3.1:8b

**User Flows**:
1. User types question
2. AI responds with context from course
3. User asks follow-up
4. Conversation continues until quota (Intermediate)

**Edge Cases**:
- Quota exceeded: Show upgrade prompt
- OLLAMA offline: Show error, retry option
- Invalid question: Guide user to rephrase

### 05_📊_Progress.py - Progress Dashboard

**Purpose**: Track learning progress, streaks, and achievements.

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ 📊 Your Progress                                             │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│ │ Courses  │ │ Streak   │ │ Hours    │ │ Badges   │        │
│ │    5     │ │ 14 days  │ │   45h    │ │   12     │        │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│                                                               │
│ Course Progress                                              │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ Data Science 101            ████████████░░░░  75%    │   │
│ │ 9/12 lessons • 2/3 quizzes                           │   │
│ │                                                       │   │
│ │ Machine Learning Basics     ████░░░░░░░░░░░░  25%    │   │
│ │ 3/15 lessons • 0/5 quizzes                           │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                               │
│ Learning Streak Calendar                                     │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ M  T  W  T  F  S  S                                  │   │
│ │ ✓  ✓  ✓  ✓  ✓  -  ✓   Current Week                  │   │
│ │ ✓  ✓  ✓  ✓  ✓  ✓  ✓   Last Week                     │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                               │
│ ┌─ Intermediate+ Analytics ────────────────────────────┐   │
│ │ 📈 Time Spent by Topic                                │   │
│ │ [Bar Chart: Pandas 12h, ML 8h, Stats 6h...]          │   │
│ │                                                        │   │
│ │ 🎯 Quiz Performance                                   │   │
│ │ [Line Chart: Scores over time]                        │   │
│ └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Components Used**:
- Progress Tracker
- Streak calendar
- Analytics charts (tier-gated)

**Tier Variations**:
- **Basic**: Basic progress bars and streak
- **Intermediate**: Detailed analytics, charts
- **Advanced**: Export progress, goal setting

### 06_🏆_Achievements.py - Achievements

**Purpose**: Display earned badges, rewards, and milestones.

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ 🏆 Achievements                                              │
├─────────────────────────────────────────────────────────────┤
│ Your Badges (12 earned, 8 locked)                           │
│                                                               │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│ │ 🎓      │ │ 📊      │ │ 🔥      │ │ 💻      │           │
│ │First    │ │Data     │ │Week     │ │Code     │           │
│ │Course   │ │Wrangler │ │Warrior  │ │Master   │           │
│ │✓ Earned │ │✓ Earned │ │✓ Earned │ │🔒 Locked│           │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘           │
│                                                               │
│ Recent Achievements                                          │
│ 🏆 Data Wrangler - Completed all pandas exercises           │
│    Earned on Jan 10, 2026                                   │
│                                                               │
│ 🔥 Week Warrior - 7-day learning streak                     │
│    Earned on Jan 8, 2026                                    │
│                                                               │
│ Next Milestones                                              │
│ 📚 Finish "Data Science 101" - 3 lessons remaining          │
│ 🎯 Ace all quizzes with 90%+ - 2/5 complete                │
│ 💯 100-hour learner - 55 hours remaining                    │
└─────────────────────────────────────────────────────────────┘
```

**Components Used**:
- Badge grid
- Achievement cards
- Progress to next milestones

### 07_📜_Certificates.py - Certificates

**Purpose**: View and download completion certificates.

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ 📜 Certificates                                              │
├─────────────────────────────────────────────────────────────┤
│ ┌─ Basic Tier ─────────────────────────────────────────┐   │
│ │ 🔒 Certificates Not Available                         │   │
│ │ Upgrade to Intermediate to receive verifiable        │   │
│ │ completion certificates.                              │   │
│ │ [Upgrade Now] [Learn More]                            │   │
│ └───────────────────────────────────────────────────────┘   │
│                                                               │
│ ┌─ Intermediate+ ──────────────────────────────────────┐   │
│ │ Your Certificates (2 earned)                          │   │
│ │                                                        │   │
│ │ ┌────────────────────────────────────────────────┐   │   │
│ │ │ 📜 Data Science Fundamentals                   │   │   │
│ │ │ Completed: Dec 15, 2025                        │   │   │
│ │ │ Certificate ID: DS-2025-A1B2C3                 │   │   │
│ │ │ [Download PDF] [Verify] [Share on LinkedIn]   │   │   │
│ │ └────────────────────────────────────────────────┘   │   │
│ │                                                        │   │
│ │ ┌────────────────────────────────────────────────┐   │   │
│ │ │ 📜 Machine Learning Basics                     │   │   │
│ │ │ Completed: Jan 5, 2026                         │   │   │
│ │ │ Certificate ID: ML-2026-D4E5F6                 │   │   │
│ │ │ [Download PDF] [Verify] [Share on LinkedIn]   │   │   │
│ │ │ ✅ Professionally Signed (Advanced Tier)       │   │   │
│ │ └────────────────────────────────────────────────┘   │   │
│ └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Components Used**:
- Certificate Generator
- Verification links
- Social sharing

**Tier Variations**:
- **Basic**: No certificates
- **Intermediate**: Verifiable PDF with QR code
- **Advanced**: Professional signed certificates

### 08_💾_Datasets.py - Dataset Explorer

**Purpose**: Browse and download course datasets.

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ 💾 Datasets - Data Science 101                               │
├─────────────────────────────────────────────────────────────┤
│ Available Datasets (5 standard, 2 production-grade)         │
│                                                               │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ 📊 Customer Churn Dataset               [Standard]   │   │
│ │ 10,000 rows • 12 columns • CSV, JSON                 │   │
│ │ Customer behavior data for churn prediction          │   │
│ │                                                       │   │
│ │ [Preview] [Download CSV] [Download JSON]             │   │
│ │ [📖 Data Dictionary]                                  │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                               │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ 🏭 Production Sales Dataset    🔒 [Advanced Only]    │   │
│ │ 1M rows • 25 columns • Parquet, CSV                  │   │
│ │ Real-world sales data for advanced analytics         │   │
│ │                                                       │   │
│ │ [Upgrade to Access]                                   │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                               │
│ Dataset Preview: Customer Churn                              │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ customer_id | age | tenure | churn                   │   │
│ │ ───────────────────────────────────────────────────  │   │
│ │ C001        | 35  | 12     | 0                       │   │
│ │ C002        | 42  | 24     | 0                       │   │
│ │ C003        | 28  | 3      | 1                       │   │
│ │ ... (showing 100/10,000 rows)                        │   │
│ └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Components Used**:
- Dataset Explorer
- Data preview table
- Download buttons (tier-gated)

### 09_⚙️_Settings.py - Settings

**Purpose**: Manage license, preferences, and account settings.

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ ⚙️ Settings                                                   │
├─────────────────────────────────────────────────────────────┤
│ License Information                                          │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ Tier: Intermediate (AI Practitioner) 🔵              │   │
│ │ License Key: INT-2026-*****-*****                    │   │
│ │ Expires: Dec 31, 2026 (364 days remaining)          │   │
│ │                                                       │   │
│ │ [Upgrade to Advanced] [Renew License]                │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                               │
│ Feature Access                                               │
│ ✅ Video Downloads                                           │
│ ✅ AI Tutor (47/50 questions remaining)                     │
│ ✅ Interactive Notebooks (JupyterLite)                      │
│ ✅ Completion Certificates                                  │
│ 🔒 GPU Notebook Access (Advanced Tier)                      │
│ 🔒 Unlimited AI Tutor (Advanced Tier)                       │
│                                                               │
│ Preferences                                                  │
│ ☑ Enable analytics (anonymous usage data)                   │
│ ☑ Email notifications                                        │
│ ☐ Dark mode                                                  │
│ Video quality: [Auto ▼]                                      │
│                                                               │
│ Account Actions                                              │
│ [Export Progress Data] [Sign Out] [Delete Account]          │
└─────────────────────────────────────────────────────────────┘
```

**Components Used**:
- License info display
- Feature checklist
- Preferences form
- Account management

## Design System

### Color Palette

**Primary Colors**:
- Primary Blue: `#3b82f6`
- Secondary Purple: `#8b5cf6`
- Success Green: `#10b981`
- Warning Orange: `#f59e0b`
- Error Red: `#ef4444`

**Tier Badge Colors**:
- Basic (Foundation Builder): `#10b981` (Green)
- Intermediate (AI Practitioner): `#3b82f6` (Blue)
- Advanced (AI/ML Expert): `#8b5cf6` (Purple)
- Enterprise: `#6366f1` (Indigo)

**Neutral Colors**:
- Background: `#ffffff` (light), `#1f2937` (dark)
- Text Primary: `#111827` (light), `#f9fafb` (dark)
- Text Secondary: `#6b7280`
- Border: `#e5e7eb`

### Typography

**Font Family**:
- Primary: `'Inter', 'Segoe UI', system-ui, sans-serif`
- Monospace: `'Fira Code', 'Consolas', monospace`

**Font Sizes**:
- Heading 1: `2.5rem` (40px)
- Heading 2: `2rem` (32px)
- Heading 3: `1.5rem` (24px)
- Body: `1rem` (16px)
- Small: `0.875rem` (14px)
- Caption: `0.75rem` (12px)

### Icons

Use emoji or Streamlit's built-in icon support:
- 🏠 Home
- 📚 Courses
- 🎓 Learn
- 🧪 Labs
- 🤖 AI Tutor
- 📊 Progress
- 🏆 Achievements
- 📜 Certificates
- 💾 Datasets
- ⚙️ Settings

### Component Library

**Tier Badge**:
```python
def render_tier_badge(tier: str):
    """Render tier badge"""
    badges = {
        'basic': ('🟢', 'Foundation Builder', '#10b981'),
        'intermediate': ('🔵', 'AI Practitioner', '#3b82f6'),
        'advanced': ('🟣', 'AI/ML Expert', '#8b5cf6'),
        'enterprise': ('🔷', 'Enterprise', '#6366f1')
    }
    
    emoji, label, color = badges.get(tier, badges['basic'])
    st.markdown(
        f'<span style="background-color:{color}; color:white; '
        f'padding:4px 12px; border-radius:12px; font-size:14px;">'
        f'{emoji} {label}</span>',
        unsafe_allow_html=True
    )
```

**Progress Bar**:
```python
def render_progress_bar(progress: int, label: str = ""):
    """Render custom progress bar"""
    st.progress(progress / 100)
    if label:
        st.caption(f"{label}: {progress}%")
```

**Feature Lock**:
```python
def render_feature_lock(feature_name: str, required_tier: str):
    """Render locked feature indicator"""
    st.info(
        f"🔒 **{feature_name}** requires {required_tier.title()} tier\n\n"
        f"[Upgrade Now](#)"
    )
```

### Responsive Layouts

Use Streamlit columns for responsive design:

```python
# Desktop: 3 columns, Mobile: 1 column
col1, col2, col3 = st.columns([1, 1, 1])

# Sidebar for navigation (auto-responsive)
with st.sidebar:
    st.navigation([...])
```

## UX Patterns

### 1. Upgrade Prompts (Non-Intrusive)

**Good**:
- Show feature, then explain it's locked
- Clear value proposition
- Non-modal, dismissible
- Compare tiers side-by-side

**Bad**:
- Block access with modal
- Constant nagging
- Unclear pricing
- Hide what user is missing

**Example**:
```python
def show_upgrade_prompt(feature: str):
    """Non-intrusive upgrade prompt"""
    with st.expander("🔓 Unlock This Feature"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Current Tier**: Basic")
            st.write("❌ Feature locked")
        with col2:
            st.write("**Intermediate Tier**")
            st.write("✅ Feature unlocked")
            st.write("**$247/year**")
            st.button("Upgrade")
```

### 2. Locked Feature States

Visual indication of locked features:

```python
# Disabled button with tooltip
st.button(
    "Download Video 🔒",
    disabled=True,
    help="Available in Intermediate tier"
)
```

### 3. Loading States

Show loading for async operations:

```python
with st.spinner("Loading course materials..."):
    data = load_course_data()
```

### 4. Error Handling

Clear, actionable error messages:

```python
try:
    result = api_call()
except APIError as e:
    st.error(f"⚠️ {e.message}")
    if st.button("Retry"):
        st.rerun()
```

### 5. Success Feedback

Confirm successful actions:

```python
st.success("✅ Lesson marked complete!")
st.balloons()  # For achievements
```

### 6. Quota Warnings

Warn before quota is exceeded:

```python
if remaining <= 5:
    st.warning(f"⚠️ Only {remaining} AI Tutor questions remaining this month")
```

## Accessibility

### WCAG 2.1 AA Compliance

- **Color Contrast**: Minimum 4.5:1 for text
- **Keyboard Navigation**: All features accessible via keyboard
- **Screen Readers**: Proper ARIA labels
- **Focus Indicators**: Visible focus states
- **Alt Text**: For all images and icons

### Implementation

```python
# Accessible button
st.button(
    "Download",
    key="download_btn",
    help="Download video for offline viewing"
)

# Accessible link
st.markdown(
    '<a href="/course/ml-101" aria-label="Go to ML 101 course">ML 101</a>',
    unsafe_allow_html=True
)
```

## Performance

### Optimization Techniques

1. **Lazy Loading**: Load content on demand
2. **Caching**: Use `@st.cache_data` for expensive operations
3. **Pagination**: Limit initial data fetching
4. **Debouncing**: For search inputs
5. **Virtual Scrolling**: For long lists

**Example**:
```python
@st.cache_data(ttl=300)
def load_course_list():
    """Load and cache course list"""
    return api.get_courses()

# Pagination
page = st.number_input("Page", min_value=1, value=1)
courses = load_course_list()
paginated = courses[(page-1)*10:page*10]
```

## Related Documentation

- [Architecture](./ARCHITECTURE.md)
- [Components](./COMPONENTS.md)
- [Feature Gates](./FEATURE_GATES.md)
- [Integration Guide](./INTEGRATION.md)
- [Deployment Guide](./DEPLOYMENT.md)
