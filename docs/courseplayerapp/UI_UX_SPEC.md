# UI/UX Specification

This document defines the user interface and user experience design for CoursePlayerApp, including page layouts, navigation flows, design system, and tier-specific adaptations.

## Table of Contents

1. [Page Structure](#page-structure)
2. [Page Specifications](#page-specifications)
3. [Design System](#design-system)
4. [User Flows](#user-flows)
5. [Responsive Behavior](#responsive-behavior)

---

## Page Structure

CoursePlayerApp uses Streamlit's multi-page app structure with emoji-based navigation:

```
courseplayerapp/pages/
├── 00_🏠_Home.py                  # Dashboard and quick access
├── 01_📚_Course_Browser.py        # Course catalog
├── 02_🎓_Learn.py                 # Main learning interface
├── 03_🧪_Labs.py                  # Interactive labs
├── 04_🤖_AI_Tutor.py             # AI tutoring chat
├── 05_📊_Progress.py              # Analytics and progress
├── 06_🏆_Achievements.py          # Badges and rewards
├── 07_📜_Certificates.py          # Certificate gallery
├── 08_💾_Datasets.py              # Dataset explorer
└── 09_⚙️_Settings.py             # License and preferences
```

---

## Page Specifications

### 1. Home Page (`00_🏠_Home.py`)

#### Purpose
Central dashboard providing quick access to recent activity, course progress, and key features.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ 🏠 Welcome back, [User Name]!                    [Tier Badge]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────┐  ┌──────────────────────────────────┐  │
│ │ Continue Learning   │  │ Daily Streak (Intermediate+)      │  │
│ │                     │  │ 🔥 7 days                         │  │
│ │ Course: ML Basics   │  │ Keep it going!                    │  │
│ │ Progress: 45%       │  │                                   │  │
│ │ [Continue →]        │  │ XP Today: 150 / Level 12          │  │
│ └─────────────────────┘  └──────────────────────────────────┘  │
│                                                                 │
│ Quick Actions                                                   │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│ │ 🎓 Learn │ │ 🧪 Labs  │ │ 🤖 AI    │ │ 📊 Stats │          │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│                                                                 │
│ Recent Activity                                                 │
│ • Completed: Introduction to Neural Networks (2h ago)          │
│ • Started: Gradient Descent Lab (5h ago)                       │
│ • Achievement Unlocked: First Week Complete! (1d ago)          │
│                                                                 │
│ Recommended Next                                                │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ 📹 Backpropagation Explained (15 min)                   │    │
│ └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

#### Components
- **Hero Section**: Personalized greeting with tier badge
- **Continue Learning Card**: Resume last course
- **Streak Tracker** (Intermediate+): Daily streak and XP
- **Quick Actions**: Direct links to key features
- **Recent Activity**: Last 5 activities
- **Recommended Next**: AI-suggested next lesson

#### Tier Variations
- **Basic**: No streak tracker, no XP display
- **Intermediate**: Full streak and XP tracking
- **Advanced**: Additional "Learning Insights" panel with predictions

#### State Management
```python
st.session_state.current_course_id
st.session_state.last_lesson_id
st.session_state.user_name
st.session_state.tier
```

#### Implementation
```python
import streamlit as st
from courseplayerapp.integrations.coursesgtm_client import CoursesGTMClient

def render_home_page():
    st.title(f"🏠 Welcome back, {st.session_state.user_name}!")
    
    # Tier badge
    tier_badge = {
        'basic': '🔵 Basic',
        'intermediate': '🟢 Intermediate',
        'advanced': '⭐ Advanced'
    }
    st.caption(tier_badge.get(st.session_state.tier, ''))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_continue_learning_card()
    
    with col2:
        if st.session_state.tier in ['intermediate', 'advanced']:
            render_streak_tracker()
    
    render_quick_actions()
    render_recent_activity()
    render_recommended_next()
```

---

### 2. Course Browser (`01_📚_Course_Browser.py`)

#### Purpose
Browse and enroll in available courses with tier-based access indicators.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ 📚 Course Catalog                                               │
├─────────────────────────────────────────────────────────────────┤
│ Search: [__________]  Category: [All ▼]  Tier: [All ▼]         │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ Machine Learning Fundamentals            [Basic] [Start] │    │
│ │ ★★★★★ (1,234 students)                                   │    │
│ │ Learn ML basics, algorithms, and Python implementation   │    │
│ │ 📹 24 videos • 🧪 8 labs • 📝 6 quizzes                  │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ Deep Learning Specialization      [Intermediate] 🔒      │    │
│ │ ★★★★☆ (856 students)                                     │    │
│ │ Advanced neural networks and deep learning techniques    │    │
│ │ 📹 36 videos • 🧪 12 labs • 📝 8 quizzes • 🤖 AI Tutor   │    │
│ │ [Upgrade to Access →]                                    │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ MLOps Professional                      [Advanced] 🔒    │    │
│ │ ★★★★★ (432 students)                                     │    │
│ │ Production ML systems, deployment, and monitoring        │    │
│ │ 📹 48 videos • 🧪 16 labs • 📜 Certificate • 🎯 Projects │    │
│ │ [Upgrade to Advanced →]                                  │    │
│ └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

#### Components
- **Search & Filters**: Text search, category, and tier filters
- **Course Cards**: Title, rating, description, features, enrollment button
- **Tier Badges**: Visual indicator of required tier
- **Lock Icons**: For inaccessible courses
- **Upgrade CTAs**: For locked courses

#### Actions
- **Start/Continue**: Enroll or continue course
- **Preview**: View course outline (modal)
- **Upgrade**: Redirect to upgrade page

---

### 3. Learn Page (`02_🎓_Learn.py`)

#### Purpose
Main learning interface with video player, slides, notes, and navigation.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ 🎓 Machine Learning Fundamentals > Module 2 > Lesson 3         │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐    │
│ │                                                         │    │
│ │         [Video Player Area]                             │    │
│ │         Introduction to Gradient Descent                │    │
│ │         Duration: 15:23 / Current: 08:45                │    │
│ │                                                         │    │
│ │ [Quality: Auto ▼] [Speed: 1x ▼] [📥 Download]          │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ [📄 Slides] [📝 Notes] [📋 Transcript] [📊 Resources]          │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ Key Concepts                                            │    │
│ │ • Gradient descent finds minimum of loss function       │    │
│ │ • Learning rate controls step size                      │    │
│ │ • Can get stuck in local minima                         │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ [⬅️ Previous Lesson]      [✅ Mark Complete]  [Next Lesson ➡️] │
└─────────────────────────────────────────────────────────────────┘
```

#### Components
- **Video Player**: Main content delivery
- **Tabbed Content**: Slides, Notes, Transcript, Resources
- **Key Concepts**: Auto-generated summary
- **Navigation**: Previous/Next, Mark Complete

#### Tier Variations
- **Basic**: Video only, no download, no transcript
- **Intermediate**: + Download, transcript (view only)
- **Advanced**: + Searchable transcript, personal annotations

---

### 4. Labs Page (`03_🧪_Labs.py`)

#### Purpose
Interactive coding environment for hands-on practice.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ 🧪 Lab: Data Preprocessing                     [Tier: Advanced] │
├─────────────────────────────────────────────────────────────────┤
│ [Instructions] [Code] [Output] [Hints]                          │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ # Cell 1: Import libraries                              │    │
│ │ import pandas as pd                                      │    │
│ │ import numpy as np                                       │    │
│ │ [▶ Run]  [In Progress...] [✅ Completed]                │    │
│ │                                                         │    │
│ │ Output:                                                 │    │
│ │ Libraries imported successfully                         │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ # Cell 2: Load dataset                                  │    │
│ │ df = pd.read_csv('data.csv')                            │    │
│ │ print(df.head())                                        │    │
│ │ [▶ Run]                                                 │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ [💾 Save Progress] [🔄 Restart Kernel] [📥 Export Notebook]    │
└─────────────────────────────────────────────────────────────────┘
```

#### Components
- **Notebook Interface**: Code cells with execution
- **Tab Navigation**: Instructions, Code, Output, Hints
- **Action Buttons**: Run, Save, Restart, Export
- **Progress Indicators**: Cell completion status

#### Tier Variations
- **Basic**: Static HTML view only
- **Intermediate**: JupyterLite (browser execution)
- **Advanced**: Full JupyterLab with persistent storage

---

### 5. AI Tutor Page (`04_🤖_AI_Tutor.py`)

#### Purpose
AI-powered tutoring chat interface with course context.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ 🤖 AI Tutor - Machine Learning Fundamentals                     │
├─────────────────────────────────────────────────────────────────┤
│ Questions remaining: [████████░░] 45/50 (Intermediate)          │
│ Model: llama3.2:3b • Resets: Feb 1, 2024                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 👤 You:                                                         │
│ What's the difference between gradient descent and SGD?         │
│                                                                 │
│ 🤖 AI Tutor:                                                    │
│ Great question! Let me explain the key differences:             │
│                                                                 │
│ **Gradient Descent (GD):**                                      │
│ • Uses entire dataset for each update                           │
│ • More accurate but slower                                      │
│ • Better for small datasets                                     │
│                                                                 │
│ **Stochastic Gradient Descent (SGD):**                          │
│ • Uses one sample at a time                                     │
│ • Faster but more noisy                                         │
│ • Better for large datasets                                     │
│                                                                 │
│ Here's a Python example:                                        │
│ ```python                                                       │
│ # GD update                                                     │
│ gradient = compute_gradient(X, y, w)                            │
│ w = w - learning_rate * gradient                                │
│                                                                 │
│ # SGD update (one sample)                                       │
│ for xi, yi in zip(X, y):                                        │
│     gradient = compute_gradient(xi, yi, w)                      │
│     w = w - learning_rate * gradient                            │
│ ```                                                             │
│                                                                 │
│ Would you like me to explain mini-batch GD as well?             │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Ask a question... [Send]                                        │
│                                                                 │
│ [📥 Export Chat] (Advanced only) [🔄 New Conversation]          │
└─────────────────────────────────────────────────────────────────┘
```

#### Components
- **Quota Display**: Remaining questions (Intermediate)
- **Chat History**: Scrollable conversation
- **Input Area**: Question input with send button
- **Export Button**: Download chat (Advanced)
- **Model Info**: Current model and context

#### Tier Variations
- **Basic**: Blocked with upgrade prompt
- **Intermediate**: 50 questions/month, llama3.2:3b
- **Advanced**: Unlimited, llama3.1:8b, export capability

---

### 6. Progress Page (`05_📊_Progress.py`)

#### Purpose
Detailed learning analytics, progress tracking, and gamification.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ 📊 Your Learning Progress                                       │
├─────────────────────────────────────────────────────────────────┤
│ Current Course: Machine Learning Fundamentals                   │
│ [████████████████████░░░░░░░] 65% Complete                      │
│                                                                 │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│ │ 🔥 Streak│ │ 📈 Level │ │ ⏱️ Time  │ │ 🎯 XP    │           │
│ │ 12 days  │ │ 15       │ │ 24.5 hrs│ │ 3,450    │           │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│                                                                 │
│ Daily Activity (Last 30 Days)                                   │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │     [Bar Chart: Time Spent Per Day]                     │    │
│ │  60min |  █                                             │    │
│ │  40min |  █ █     █ █                                   │    │
│ │  20min |█ █ █ █ █ █ █ █                                 │    │
│ │         └────────────────────────────────────           │    │
│ │          1  5  10  15  20  25  30                       │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ Module Progress                                                 │
│ ✅ Module 1: Introduction (100%)                               │
│ ⏳ Module 2: Algorithms (65%)                                  │
│ 🔒 Module 3: Neural Networks (0%)                              │
│ 🔒 Module 4: Deployment (0%)                                   │
│                                                                 │
│ Strong Topics                 │ Needs Review                   │
│ ✅ Linear Regression (95%)    │ ⚠️ Backpropagation (45%)      │
│ ✅ Data Preprocessing (90%)   │ ⚠️ Regularization (52%)       │
└─────────────────────────────────────────────────────────────────┘
```

#### Components
- **Course Progress Bar**: Overall completion
- **Metric Cards**: Streak, Level, Time, XP
- **Activity Chart**: Daily time spent (Plotly)
- **Module Breakdown**: Per-module progress
- **Topic Analysis**: Strong vs weak areas

#### Tier Variations
- **Basic**: Simple progress bar only
- **Intermediate**: Full analytics and gamification
- **Advanced**: + ML predictions (completion date, final score)

---

### 7. Achievements Page (`06_🏆_Achievements.py`)

#### Purpose
Display unlocked achievements, badges, and rewards.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ 🏆 Achievements & Rewards                                       │
├─────────────────────────────────────────────────────────────────┤
│ Level 15 • 3,450 XP • 12 Achievements Unlocked                  │
│                                                                 │
│ Recent Unlocks                                                  │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│ │ 🔥          │ │ 📚          │ │ 🧪          │               │
│ │ Week Streak │ │ Course Half │ │ Lab Master  │               │
│ │ 7 days      │ │ 50% done    │ │ 5 labs done │               │
│ │ Unlocked!   │ │ Unlocked!   │ │ Unlocked!   │               │
│ └─────────────┘ └─────────────┘ └─────────────┘               │
│                                                                 │
│ All Achievements (12/30)                                        │
│ ✅ First Lesson                 ✅ Week Warrior                 │
│ ✅ Quiz Master                  ✅ Lab Expert                   │
│ ✅ AI Curious (Int+)            🔒 Course Complete              │
│ 🔒 Speed Learner                🔒 Perfect Score                │
│ 🔒 Certificate Earner (Int+)   🔒 Code Reviewer (Adv)          │
│                                                                 │
│ Rare Achievements (Advanced Only)                               │
│ 🔒 Elite Learner - Complete 5 courses with 95%+ score          │
│ 🔒 Marathon Runner - 30-day streak                             │
│                                                                 │
│ Leaderboard (Team/Enterprise)                                   │
│ 🥇 Alice Chen - 5,200 XP                                       │
│ 🥈 Bob Wilson - 4,800 XP                                       │
│ 🥉 You - 3,450 XP                                              │
└─────────────────────────────────────────────────────────────────┘
```

#### Components
- **Progress Summary**: Level, XP, total achievements
- **Recent Unlocks**: Last 3 achievements with animations
- **Achievement Grid**: All achievements (locked/unlocked)
- **Rare Achievements**: Advanced tier exclusives
- **Leaderboard**: Team/Enterprise feature

---

### 8. Certificates Page (`07_📜_Certificates.py`)

#### Purpose
View, download, and share earned certificates.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ 📜 Your Certificates                             [Intermediate] │
├─────────────────────────────────────────────────────────────────┤
│ Upgrade to Intermediate to earn verifiable certificates!        │
│ [View Sample Certificate] [🚀 Upgrade Now]                      │
│ (Basic tier sees upgrade prompt)                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Earned Certificates (Intermediate/Advanced)                     │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ 🎓 Machine Learning Fundamentals                        │    │
│ │ Completed: January 15, 2024 • Score: 92%               │    │
│ │ ✅ Verified • Certificate ID: ML-2024-001234            │    │
│ │                                                         │    │
│ │ [📥 Download PDF] [🔗 Share on LinkedIn] [👁️ Preview]  │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ 🎓 Data Science Essentials                              │    │
│ │ Completed: December 20, 2023 • Score: 88%              │    │
│ │ ✅ Verified • Certificate ID: DS-2023-005678            │    │
│ │ 🔏 Digitally Signed (Advanced tier)                     │    │
│ │                                                         │    │
│ │ [📥 Download PDF] [🔗 LinkedIn] [👁️ Preview] [🔍 Verify]│    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ Certificate Verification                                        │
│ Enter Certificate ID: [___________] [Verify]                    │
└─────────────────────────────────────────────────────────────────┘
```

---

### 9. Datasets Page (`08_💾_Datasets.py`)

#### Purpose
Browse, preview, and download course datasets.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ 💾 Course Datasets                            [Tier: Advanced]  │
├─────────────────────────────────────────────────────────────────┤
│ Search: [__________]  Type: [All ▼]  Course: [ML Fund. ▼]      │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ 📊 MNIST Handwritten Digits                             │    │
│ │ 60,000 images • 10 classes • 25 MB                      │    │
│ │ Format: PNG images + CSV labels                         │    │
│ │                                                         │    │
│ │ [👁️ Preview] [📥 Download] (Intermediate+)             │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ Dataset Preview (Intermediate+)                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ Showing first 100 rows (Intermediate)                   │    │
│ │ Showing all rows (Advanced)                             │    │
│ │                                                         │    │
│ │   ID | Digit | Label | File                            │    │
│ │ ─────┼───────┼───────┼──────────                       │    │
│ │   1  |   5   |   5   | img_0001.png                    │    │
│ │   2  |   0   |   0   | img_0002.png                    │    │
│ │  ... |  ...  |  ...  | ...                             │    │
│ └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

### 10. Settings Page (`09_⚙️_Settings.py`)

#### Purpose
Manage license, preferences, and account settings.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ ⚙️ Settings                                                     │
├─────────────────────────────────────────────────────────────────┤
│ [License] [Preferences] [Account] [About]                       │
│                                                                 │
│ License Information                                             │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ Status: ✅ Active                                       │    │
│ │ Tier: 🟢 Intermediate                                   │    │
│ │ Expires: December 31, 2024                              │    │
│ │ Renewal: Auto-renew enabled                             │    │
│ │                                                         │    │
│ │ [🚀 Upgrade to Advanced] [🔄 Manage Subscription]       │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ Preferences                                                     │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ Theme: [Auto ▼] (Light, Dark, Auto)                    │    │
│ │ Language: [English ▼]                                   │    │
│ │ Video Quality: [Auto ▼]                                 │    │
│ │ Notifications: [✅] Email [✅] In-app                   │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ Offline Mode (Advanced Only)                                    │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ Download courses for offline access (30 days)           │    │
│ │ [📥 Download Current Course] [Manage Downloads]         │    │
│ └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Design System

### Color Scheme

```python
THEME = {
    'primary': '#1E88E5',      # Blue - primary actions
    'secondary': '#FFC107',    # Amber - highlights
    'success': '#4CAF50',      # Green - success states
    'warning': '#FF9800',      # Orange - warnings
    'error': '#F44336',        # Red - errors
    'info': '#2196F3',         # Light blue - info
    
    # Tier colors
    'basic': '#90A4AE',        # Gray
    'intermediate': '#66BB6A', # Green
    'advanced': '#FFD54F',     # Gold
    
    # Backgrounds
    'bg_primary': '#FFFFFF',
    'bg_secondary': '#F5F5F5',
    'bg_dark': '#263238',
    
    # Text
    'text_primary': '#212121',
    'text_secondary': '#757575',
    'text_light': '#FFFFFF'
}
```

### Typography

```python
TYPOGRAPHY = {
    'font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    'heading_1': '2.5rem',
    'heading_2': '2rem',
    'heading_3': '1.5rem',
    'body': '1rem',
    'caption': '0.875rem',
    'small': '0.75rem'
}
```

### Spacing

```python
SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '16px',
    'lg': '24px',
    'xl': '32px',
    'xxl': '48px'
}
```

### Component Styles

**Button Styles:**
```python
BUTTONS = {
    'primary': {
        'background': THEME['primary'],
        'color': THEME['text_light'],
        'border': 'none',
        'padding': '12px 24px',
        'border_radius': '8px'
    },
    'secondary': {
        'background': 'transparent',
        'color': THEME['primary'],
        'border': f"2px solid {THEME['primary']}",
        'padding': '10px 22px',
        'border_radius': '8px'
    },
    'disabled': {
        'background': '#E0E0E0',
        'color': '#9E9E9E',
        'cursor': 'not-allowed'
    }
}
```

---

## User Flows

### 1. First-Time Onboarding

```
Start → License Activation → Tier Selection → Profile Setup → 
Course Selection → Tutorial Walkthrough → Begin Learning
```

### 2. License Activation

```
Enter License Key → Validate with CoursesGTM → 
Success: Store in Session → Redirect to Home
Failure: Show Error → Retry or Contact Support
```

### 3. Starting a Course

```
Course Browser → Select Course → Check Access → 
Has Access: Go to Learn Page
No Access: Show Upgrade Prompt → Upgrade or Cancel
```

### 4. Completing a Lesson

```
Watch Video → Mark Complete → Update Progress → 
Check for Achievement → Show Celebration → 
Suggest Next Lesson → Continue or Exit
```

### 5. Asking AI Tutor Question

```
Navigate to AI Tutor → Check Quota → 
Has Quota: Enter Question → Stream Response → Save to History
No Quota: Show Upgrade Prompt or Wait for Reset
```

### 6. Upgrading Tier

```
Click Upgrade → View Tier Comparison → 
Select Target Tier → Redirect to LemonSqueezy → 
Complete Payment → Receive License → Validate → 
Update Session → Show Success → Refresh Features
```

---

## Responsive Behavior

### Desktop (> 1024px)
- Full sidebar navigation
- Multi-column layouts
- Expanded components
- Video player: 16:9 ratio

### Tablet (768px - 1024px)
- Collapsible sidebar
- 2-column layouts
- Compact components
- Video player: responsive

### Mobile (< 768px)
- Bottom navigation
- Single-column layout
- Stacked components
- Full-width video player

### Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader optimization
- High contrast mode
- Focus indicators
- Alt text for images

---

This UI/UX specification provides comprehensive guidance for implementing a cohesive, tier-aware, and user-friendly interface for CoursePlayerApp.
