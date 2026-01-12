# CoursePlayerApp - Progress Tracking Specification

## Overview

Progress tracking is essential for student motivation and course completion. CoursePlayerApp tracks comprehensive learning metrics and provides visual feedback through dashboards and analytics.

---

## Tracked Metrics

### 1. Video Progress

**Per Video Metrics**:
- **Watched status**: Boolean (has user started watching?)
- **Completion percentage**: 0-100% (how much of video was watched)
- **Last position**: Timestamp where user stopped (for resume)
- **Time spent**: Total seconds spent watching (including rewinds)
- **First watched**: Timestamp of first view
- **Last watched**: Timestamp of most recent view
- **Watch count**: Number of times user watched this video

**Example**:
```json
{
  "video_id": "ai-03-module-01-video-02",
  "title": "Understanding Transformers Architecture",
  "watched": true,
  "completion_percentage": 87,
  "last_position_seconds": 2340,
  "duration_seconds": 2700,
  "time_spent_seconds": 3150,
  "first_watched_at": "2026-01-10T14:30:00Z",
  "last_watched_at": "2026-01-12T10:15:00Z",
  "watch_count": 2
}
```

### 2. Slides Progress

**Per Slide Deck Metrics**:
- **Viewed status**: Boolean (has user opened slides?)
- **Slides viewed**: Number of individual slides viewed
- **Total slides**: Total slides in deck
- **Time spent**: Total seconds spent viewing slides
- **Downloaded**: Boolean (did user download slides?) - Tier-dependent
- **Export format**: PDF/PPTX - Tier-dependent

**Example**:
```json
{
  "slide_deck_id": "ai-03-module-01-slides",
  "title": "Transformer Architecture Slides",
  "viewed": true,
  "slides_viewed": 42,
  "total_slides": 50,
  "completion_percentage": 84,
  "time_spent_seconds": 1800,
  "downloaded": true,
  "download_format": "pdf",
  "first_viewed_at": "2026-01-10T15:00:00Z",
  "last_viewed_at": "2026-01-12T11:00:00Z"
}
```

### 3. Lab Progress

**Per Lab Metrics**:
- **Started**: Boolean
- **Completed**: Boolean
- **Score**: 0-100 (if graded)
- **Attempts**: Number of attempts
- **Time spent**: Total seconds in lab
- **Code submissions**: Number of code runs
- **Hints used**: Number of hints requested

**Example**:
```json
{
  "lab_id": "ai-03-module-01-lab-01",
  "title": "Build a Simple Transformer",
  "started": true,
  "completed": true,
  "score": 95,
  "max_score": 100,
  "attempts": 2,
  "time_spent_seconds": 3600,
  "code_submissions": 8,
  "hints_used": 1,
  "first_attempt_at": "2026-01-11T09:00:00Z",
  "completed_at": "2026-01-11T10:30:00Z"
}
```

### 4. Quiz Progress

**Per Quiz Metrics**:
- **Taken**: Boolean
- **Score**: Points earned
- **Max score**: Total possible points
- **Percentage**: Score as percentage
- **Attempts**: Number of attempts
- **Best score**: Highest score across attempts
- **Time taken**: Seconds to complete
- **Questions correct**: Number of correct answers

**Example**:
```json
{
  "quiz_id": "ai-03-module-01-quiz",
  "title": "Transformers Knowledge Check",
  "taken": true,
  "score": 8,
  "max_score": 10,
  "percentage": 80,
  "attempts": 2,
  "best_score": 8,
  "time_taken_seconds": 600,
  "questions_correct": 8,
  "questions_total": 10,
  "first_attempt_at": "2026-01-11T14:00:00Z",
  "last_attempt_at": "2026-01-11T16:00:00Z"
}
```

### 5. Module Progress

**Per Module Metrics**:
- **Overall completion**: 0-100% (weighted average of components)
- **Videos completed**: Count and percentage
- **Slides viewed**: Count and percentage
- **Labs completed**: Count and percentage
- **Quizzes passed**: Count and percentage
- **Time spent**: Total seconds in module
- **Status**: Not Started | In Progress | Completed

**Completion Formula**:
```python
def calculate_module_completion(module_data: dict) -> float:
    """
    Calculate module completion percentage
    
    Weights:
    - Videos: 40%
    - Slides: 10%
    - Labs: 30%
    - Quizzes: 20%
    """
    video_completion = sum(v['completion_percentage'] for v in module_data['videos']) / len(module_data['videos'])
    slides_completion = sum(s['completion_percentage'] for s in module_data['slides']) / len(module_data['slides'])
    labs_completion = sum(1 for l in module_data['labs'] if l['completed']) / len(module_data['labs']) * 100
    quiz_completion = sum(1 for q in module_data['quizzes'] if q['percentage'] >= 70) / len(module_data['quizzes']) * 100
    
    weighted_completion = (
        video_completion * 0.4 +
        slides_completion * 0.1 +
        labs_completion * 0.3 +
        quiz_completion * 0.2
    )
    
    return round(weighted_completion, 2)
```

### 6. Course Progress

**Per Course Metrics**:
- **Overall completion**: 0-100% (average of module completions)
- **Modules completed**: Count and percentage
- **Total time spent**: Seconds across all modules
- **Status**: Not Started | In Progress | Completed | Certified
- **Started date**: First access timestamp
- **Last accessed**: Most recent access timestamp
- **Estimated completion date**: Based on current pace

**Example**:
```json
{
  "course_id": "ai-03-nlp-transformers",
  "title": "Natural Language Processing with Transformers",
  "overall_progress": 67,
  "modules_completed": 2,
  "modules_total": 5,
  "total_time_spent_seconds": 25200,
  "status": "in_progress",
  "started_at": "2026-01-10T14:00:00Z",
  "last_accessed_at": "2026-01-12T10:30:00Z",
  "estimated_completion_date": "2026-01-25",
  "certificate_earned": false
}
```

### 7. Overall User Progress

**Global Metrics**:
- **Total courses**: Enrolled, in progress, completed
- **Total time spent**: Across all courses
- **Total certificates earned**: Count
- **Learning streak**: Consecutive days of activity
- **Achievement badges**: Unlocked achievements
- **AI Tutor questions asked**: Count (tier-dependent)

---

## Progress Storage Schema

### Database Tables

**Table: `user_progress`**
```sql
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    course_id VARCHAR(255) NOT NULL,
    overall_progress INT DEFAULT 0,
    total_time_spent_seconds INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'not_started',
    started_at TIMESTAMP,
    last_accessed_at TIMESTAMP,
    estimated_completion_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, course_id)
);
```

**Table: `module_progress`**
```sql
CREATE TABLE module_progress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    course_id VARCHAR(255) NOT NULL,
    module_id VARCHAR(255) NOT NULL,
    completion_percentage INT DEFAULT 0,
    time_spent_seconds INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'not_started',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, course_id, module_id)
);
```

**Table: `video_progress`**
```sql
CREATE TABLE video_progress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    video_id VARCHAR(255) NOT NULL,
    completion_percentage INT DEFAULT 0,
    last_position_seconds INT DEFAULT 0,
    duration_seconds INT,
    time_spent_seconds INT DEFAULT 0,
    watch_count INT DEFAULT 0,
    first_watched_at TIMESTAMP,
    last_watched_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, video_id)
);
```

**Table: `lab_progress`**
```sql
CREATE TABLE lab_progress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    lab_id VARCHAR(255) NOT NULL,
    started BOOLEAN DEFAULT FALSE,
    completed BOOLEAN DEFAULT FALSE,
    score INT,
    max_score INT,
    attempts INT DEFAULT 0,
    time_spent_seconds INT DEFAULT 0,
    code_submissions INT DEFAULT 0,
    hints_used INT DEFAULT 0,
    first_attempt_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, lab_id)
);
```

**Table: `quiz_progress`**
```sql
CREATE TABLE quiz_progress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    quiz_id VARCHAR(255) NOT NULL,
    score INT,
    max_score INT,
    percentage INT,
    attempts INT DEFAULT 0,
    best_score INT,
    time_taken_seconds INT,
    questions_correct INT,
    questions_total INT,
    first_attempt_at TIMESTAMP,
    last_attempt_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, quiz_id)
);
```

### JSON Structure (API Response)

Complete progress data for a user:

```json
{
  "user_id": "user123",
  "overall_stats": {
    "courses_enrolled": 3,
    "courses_in_progress": 2,
    "courses_completed": 1,
    "total_time_spent_hours": 42.5,
    "certificates_earned": 1,
    "learning_streak_days": 7,
    "last_active": "2026-01-12T10:30:00Z"
  },
  "courses": [
    {
      "course_id": "ai-03-nlp-transformers",
      "course_title": "Natural Language Processing with Transformers",
      "overall_progress": 67,
      "status": "in_progress",
      "time_spent_seconds": 25200,
      "started_at": "2026-01-10T14:00:00Z",
      "last_accessed_at": "2026-01-12T10:30:00Z",
      "modules": [
        {
          "module_id": "module-01",
          "title": "Introduction to NLP",
          "progress": 100,
          "time_spent_seconds": 7200,
          "videos": [
            {
              "video_id": "v1-intro",
              "title": "What is NLP?",
              "watched": true,
              "completion_percentage": 100,
              "time_spent_seconds": 1200
            }
          ],
          "slides": [
            {
              "slide_deck_id": "s1",
              "title": "NLP Overview",
              "viewed": true,
              "completion_percentage": 100
            }
          ],
          "labs": [
            {
              "lab_id": "lab1",
              "title": "Tokenization Basics",
              "completed": true,
              "score": 95
            }
          ],
          "quiz": {
            "quiz_id": "q1",
            "title": "NLP Fundamentals Quiz",
            "score": 8,
            "max_score": 10,
            "percentage": 80
          }
        }
      ]
    }
  ]
}
```

---

## Progress Tracker Implementation

### Core Tracker Class

```python
# utils/progress_tracker.py
from datetime import datetime
from typing import Dict, Any
from database import db

class ProgressTracker:
    """Track and update student learning progress"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
    
    def update_video_progress(
        self,
        video_id: str,
        position_seconds: int,
        duration_seconds: int
    ):
        """Update video watch progress"""
        completion_pct = min(100, int((position_seconds / duration_seconds) * 100))
        
        # Check if record exists
        existing = db.query(
            "SELECT * FROM video_progress WHERE user_id = %s AND video_id = %s",
            (self.user_id, video_id)
        )
        
        if existing:
            # Update existing record
            db.execute("""
                UPDATE video_progress
                SET completion_percentage = %s,
                    last_position_seconds = %s,
                    watch_count = watch_count + 1,
                    last_watched_at = NOW(),
                    updated_at = NOW()
                WHERE user_id = %s AND video_id = %s
            """, (completion_pct, position_seconds, self.user_id, video_id))
        else:
            # Create new record
            db.execute("""
                INSERT INTO video_progress 
                (user_id, video_id, completion_percentage, last_position_seconds, 
                 duration_seconds, watch_count, first_watched_at, last_watched_at)
                VALUES (%s, %s, %s, %s, %s, 1, NOW(), NOW())
            """, (self.user_id, video_id, completion_pct, position_seconds, duration_seconds))
        
        # Trigger module/course progress recalculation
        self._recalculate_module_progress(video_id)
    
    def update_lab_progress(
        self,
        lab_id: str,
        completed: bool = False,
        score: int = None,
        time_spent: int = 0
    ):
        """Update lab completion progress"""
        existing = db.query(
            "SELECT * FROM lab_progress WHERE user_id = %s AND lab_id = %s",
            (self.user_id, lab_id)
        )
        
        if existing:
            update_fields = [
                "attempts = attempts + 1",
                "time_spent_seconds = time_spent_seconds + %s",
                "updated_at = NOW()"
            ]
            params = [time_spent]
            
            if completed:
                update_fields.append("completed = TRUE")
                update_fields.append("completed_at = NOW()")
            
            if score is not None:
                update_fields.append("score = %s")
                params.append(score)
            
            params.extend([self.user_id, lab_id])
            
            db.execute(
                f"UPDATE lab_progress SET {', '.join(update_fields)} WHERE user_id = %s AND lab_id = %s",
                tuple(params)
            )
        else:
            db.execute("""
                INSERT INTO lab_progress
                (user_id, lab_id, started, completed, score, attempts, time_spent_seconds, first_attempt_at)
                VALUES (%s, %s, TRUE, %s, %s, 1, %s, NOW())
            """, (self.user_id, lab_id, completed, score, time_spent))
        
        self._recalculate_module_progress(lab_id)
    
    def update_quiz_progress(
        self,
        quiz_id: str,
        score: int,
        max_score: int,
        time_taken: int
    ):
        """Update quiz attempt progress"""
        percentage = int((score / max_score) * 100)
        questions_correct = score  # Assuming 1 point per question
        
        existing = db.query(
            "SELECT * FROM quiz_progress WHERE user_id = %s AND quiz_id = %s",
            (self.user_id, quiz_id)
        )
        
        if existing:
            best_score = max(existing[0]['best_score'] or 0, score)
            
            db.execute("""
                UPDATE quiz_progress
                SET score = %s,
                    percentage = %s,
                    attempts = attempts + 1,
                    best_score = %s,
                    time_taken_seconds = %s,
                    last_attempt_at = NOW(),
                    updated_at = NOW()
                WHERE user_id = %s AND quiz_id = %s
            """, (score, percentage, best_score, time_taken, self.user_id, quiz_id))
        else:
            db.execute("""
                INSERT INTO quiz_progress
                (user_id, quiz_id, score, max_score, percentage, attempts, 
                 best_score, time_taken_seconds, questions_correct, questions_total,
                 first_attempt_at, last_attempt_at)
                VALUES (%s, %s, %s, %s, %s, 1, %s, %s, %s, %s, NOW(), NOW())
            """, (self.user_id, quiz_id, score, max_score, percentage, score, 
                  time_taken, questions_correct, max_score))
        
        self._recalculate_module_progress(quiz_id)
    
    def _recalculate_module_progress(self, component_id: str):
        """Recalculate module and course progress after component update"""
        # Extract module_id and course_id from component_id
        # Assuming format: course_id-module_id-component_type-component_number
        parts = component_id.split('-')
        if len(parts) >= 3:
            course_id = f"{parts[0]}-{parts[1]}"
            module_id = f"{parts[0]}-{parts[1]}-{parts[2]}"
            
            # Recalculate module progress
            module_completion = self._calculate_module_completion(course_id, module_id)
            
            db.execute("""
                UPDATE module_progress
                SET completion_percentage = %s,
                    updated_at = NOW()
                WHERE user_id = %s AND course_id = %s AND module_id = %s
            """, (module_completion, self.user_id, course_id, module_id))
            
            # Recalculate course progress
            course_completion = self._calculate_course_completion(course_id)
            
            db.execute("""
                UPDATE user_progress
                SET overall_progress = %s,
                    last_accessed_at = NOW(),
                    updated_at = NOW()
                WHERE user_id = %s AND course_id = %s
            """, (course_completion, self.user_id, course_id))
    
    def _calculate_module_completion(self, course_id: str, module_id: str) -> int:
        """Calculate module completion based on components"""
        # Fetch all component progress for this module
        videos = db.query(
            "SELECT AVG(completion_percentage) as avg FROM video_progress WHERE user_id = %s AND video_id LIKE %s",
            (self.user_id, f"{module_id}%")
        )
        
        labs = db.query(
            "SELECT COUNT(*) FILTER (WHERE completed) as completed, COUNT(*) as total FROM lab_progress WHERE user_id = %s AND lab_id LIKE %s",
            (self.user_id, f"{module_id}%")
        )
        
        quizzes = db.query(
            "SELECT AVG(percentage) as avg FROM quiz_progress WHERE user_id = %s AND quiz_id LIKE %s",
            (self.user_id, f"{module_id}%")
        )
        
        # Calculate weighted average
        video_completion = videos[0]['avg'] or 0 if videos else 0
        lab_completion = (labs[0]['completed'] / labs[0]['total'] * 100) if labs and labs[0]['total'] > 0 else 0
        quiz_completion = quizzes[0]['avg'] or 0 if quizzes else 0
        
        weighted = (
            video_completion * 0.4 +
            lab_completion * 0.3 +
            quiz_completion * 0.3
        )
        
        return int(weighted)
    
    def _calculate_course_completion(self, course_id: str) -> int:
        """Calculate course completion as average of module completions"""
        result = db.query(
            "SELECT AVG(completion_percentage) as avg FROM module_progress WHERE user_id = %s AND course_id = %s",
            (self.user_id, course_id)
        )
        
        return int(result[0]['avg'] or 0) if result else 0
    
    def get_course_progress(self, course_id: str) -> Dict[str, Any]:
        """Get complete progress data for a course"""
        course_data = db.query(
            "SELECT * FROM user_progress WHERE user_id = %s AND course_id = %s",
            (self.user_id, course_id)
        )
        
        if not course_data:
            return None
        
        # Fetch modules
        modules = db.query(
            "SELECT * FROM module_progress WHERE user_id = %s AND course_id = %s ORDER BY module_id",
            (self.user_id, course_id)
        )
        
        # Build response
        return {
            "course_id": course_id,
            "overall_progress": course_data[0]['overall_progress'],
            "status": course_data[0]['status'],
            "time_spent_seconds": course_data[0]['total_time_spent_seconds'],
            "started_at": course_data[0]['started_at'].isoformat() if course_data[0]['started_at'] else None,
            "last_accessed_at": course_data[0]['last_accessed_at'].isoformat() if course_data[0]['last_accessed_at'] else None,
            "modules": [self._format_module_data(m) for m in modules]
        }
    
    def _format_module_data(self, module: dict) -> dict:
        """Format module progress data"""
        return {
            "module_id": module['module_id'],
            "progress": module['completion_percentage'],
            "time_spent_seconds": module['time_spent_seconds'],
            "status": module['status']
        }
```

---

## Visualization Components

### Progress Bars

```python
# components/progress_visualizations.py
import streamlit as st
import plotly.graph_objects as go

def render_progress_bar(label: str, progress: int, color: str = "blue"):
    """Render a simple progress bar"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress / 100)
    with col2:
        st.metric(label, f"{progress}%")


def render_course_progress_card(course_data: dict):
    """Render a course progress card"""
    st.subheader(course_data['title'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Progress", f"{course_data['overall_progress']}%")
    
    with col2:
        hours = course_data['time_spent_seconds'] / 3600
        st.metric("Time Spent", f"{hours:.1f} hrs")
    
    with col3:
        st.metric("Modules", f"{course_data['modules_completed']}/{course_data['modules_total']}")
    
    st.progress(course_data['overall_progress'] / 100)
    
    if course_data['overall_progress'] >= 80:
        st.success("✅ Ready for certification exam!")
    elif course_data['overall_progress'] >= 50:
        st.info("📚 Halfway there! Keep going!")
```

### Time Spent Chart

```python
def render_time_spent_chart(time_data: list):
    """Render time spent line chart (last 30 days)"""
    import plotly.express as px
    import pandas as pd
    
    df = pd.DataFrame(time_data)
    df['date'] = pd.to_datetime(df['date'])
    df['hours'] = df['seconds'] / 3600
    
    fig = px.line(
        df,
        x='date',
        y='hours',
        title='Daily Learning Time (Last 30 Days)',
        labels={'hours': 'Hours', 'date': 'Date'}
    )
    
    fig.update_layout(
        hovermode='x unified',
        xaxis_title='Date',
        yaxis_title='Hours Spent'
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

### Completion Heatmap (Advanced Tier)

```python
def render_completion_heatmap(activity_data: list):
    """Render GitHub-style activity heatmap (Advanced tier only)"""
    import plotly.figure_factory as ff
    import pandas as pd
    
    # Prepare data
    df = pd.DataFrame(activity_data)
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.isocalendar().week
    df['weekday'] = df['date'].dt.dayofweek
    
    # Pivot for heatmap
    heatmap_data = df.pivot(index='weekday', columns='week', values='minutes')
    
    # Create figure
    fig = ff.create_annotated_heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns.tolist(),
        y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        colorscale='Greens',
        showscale=True
    )
    
    fig.update_layout(
        title='Learning Activity Heatmap',
        xaxis_title='Week',
        yaxis_title='Day'
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

### Quiz Performance Chart

```python
def render_quiz_performance(quiz_data: list):
    """Render quiz scores bar chart"""
    import plotly.express as px
    import pandas as pd
    
    df = pd.DataFrame(quiz_data)
    
    fig = px.bar(
        df,
        x='quiz_title',
        y='percentage',
        title='Quiz Performance',
        labels={'percentage': 'Score (%)', 'quiz_title': 'Quiz'},
        color='percentage',
        color_continuous_scale='RdYlGn',
        range_color=[0, 100]
    )
    
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Passing: 70%")
    
    st.plotly_chart(fig, use_container_width=True)
```

---

## Achievement Badges

### Badge System

```python
# utils/achievements.py
ACHIEVEMENTS = {
    "first_video": {
        "title": "First Steps",
        "description": "Watched your first video",
        "icon": "🎬",
        "condition": lambda progress: progress['videos_watched'] >= 1
    },
    "course_starter": {
        "title": "Course Starter",
        "description": "Started your first course",
        "icon": "🚀",
        "condition": lambda progress: progress['courses_started'] >= 1
    },
    "quiz_master": {
        "title": "Quiz Master",
        "description": "Scored 100% on a quiz",
        "icon": "🏆",
        "condition": lambda progress: any(q['percentage'] == 100 for q in progress['quizzes'])
    },
    "week_streak": {
        "title": "Week Warrior",
        "description": "7-day learning streak",
        "icon": "🔥",
        "condition": lambda progress: progress['learning_streak'] >= 7
    },
    "lab_champion": {
        "title": "Lab Champion",
        "description": "Completed 10 labs",
        "icon": "🧪",
        "condition": lambda progress: progress['labs_completed'] >= 10
    },
    "course_complete": {
        "title": "Course Completer",
        "description": "Completed your first course",
        "icon": "🎓",
        "condition": lambda progress: progress['courses_completed'] >= 1
    }
}

def check_achievements(user_progress: dict) -> list:
    """Check which achievements user has earned"""
    earned = []
    
    for achievement_id, achievement in ACHIEVEMENTS.items():
        if achievement['condition'](user_progress):
            earned.append({
                "id": achievement_id,
                "title": achievement['title'],
                "description": achievement['description'],
                "icon": achievement['icon']
            })
    
    return earned


def render_achievement_badges(earned_achievements: list):
    """Display earned achievement badges"""
    st.subheader("🏅 Achievements")
    
    cols = st.columns(4)
    for i, achievement in enumerate(earned_achievements):
        with cols[i % 4]:
            st.markdown(f"### {achievement['icon']}")
            st.caption(achievement['title'])
            st.caption(achievement['description'])
```

---

## Progress Export (Tier-Based)

### CSV Export (Intermediate & Advanced)

```python
# utils/progress_export.py
import csv
import io
from datetime import datetime

def export_progress_csv(user_progress: dict) -> bytes:
    """Export progress as CSV (Intermediate tier)"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Course', 'Module', 'Component', 'Type', 'Progress %', 'Time Spent (min)', 'Status'])
    
    # Data rows
    for course in user_progress['courses']:
        for module in course['modules']:
            for video in module.get('videos', []):
                writer.writerow([
                    course['course_title'],
                    module['title'],
                    video['title'],
                    'Video',
                    video['completion_percentage'],
                    video['time_spent_seconds'] / 60,
                    'Completed' if video['completion_percentage'] == 100 else 'In Progress'
                ])
            
            for lab in module.get('labs', []):
                writer.writerow([
                    course['course_title'],
                    module['title'],
                    lab['title'],
                    'Lab',
                    100 if lab['completed'] else 0,
                    lab.get('time_spent_seconds', 0) / 60,
                    'Completed' if lab['completed'] else 'Not Completed'
                ])
    
    return output.getvalue().encode('utf-8')
```

### JSON Export (Advanced)

```python
def export_progress_json(user_progress: dict) -> str:
    """Export progress as JSON (Advanced tier)"""
    import json
    return json.dumps(user_progress, indent=2)
```

---

## Tier-Specific Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| **Progress Bars** | ✅ | ✅ | ✅ |
| **Time Tracking** | ❌ | ✅ | ✅ |
| **Time Spent Charts** | ❌ | ✅ | ✅ |
| **Heatmap** | ❌ | ❌ | ✅ |
| **Quiz Analytics** | ✅ Basic | ✅ Detailed | ✅ Advanced |
| **Export CSV** | ❌ | ✅ | ✅ |
| **Export JSON** | ❌ | ❌ | ✅ |
| **Achievement Badges** | ✅ | ✅ | ✅ |
| **Predictive Analytics** | ❌ | ❌ | ✅ |

---

## Testing

```python
# tests/test_progress_tracker.py
def test_video_progress_update():
    tracker = ProgressTracker("test_user")
    tracker.update_video_progress("video-123", position_seconds=600, duration_seconds=1200)
    
    progress = tracker.get_video_progress("video-123")
    assert progress['completion_percentage'] == 50

def test_module_completion_calculation():
    tracker = ProgressTracker("test_user")
    completion = tracker._calculate_module_completion("ai-03", "module-01")
    assert 0 <= completion <= 100
```

---

## Conclusion

This comprehensive progress tracking system:
- **Motivates learners**: Visual progress indicators
- **Enables insights**: Analytics and charts
- **Supports tiers**: Feature-gated visualizations
- **Drives completion**: Gamification with badges

The system balances granular tracking with performance, using database aggregation and caching where appropriate.
