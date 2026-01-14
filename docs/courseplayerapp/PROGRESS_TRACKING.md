# Progress Tracking Specification

## Overview

CoursePlayerApp implements a comprehensive progress tracking system that monitors student learning activities, calculates completion metrics, and provides insightful visualizations. The system adapts detail level based on subscription tier while maintaining accurate records for all users.

---

## Tracked Metrics

### Core Metrics (All Tiers)

1. **Video Progress**
   - Videos started
   - Videos completed (≥95% watched)
   - Watch time per video
   - Overall video completion percentage

2. **Slide Progress**
   - Slides viewed
   - Slide decks completed
   - Time spent on slides

3. **Lab Progress**
   - Labs attempted
   - Labs completed
   - Lab scores
   - Time spent in SimulationPlayer

4. **Quiz Progress**
   - Quizzes taken
   - Quiz scores
   - Number of attempts
   - Best score achieved

5. **Exam Progress**
   - Exams attempted
   - Exam scores
   - Pass/fail status
   - Certification status

6. **Overall Progress**
   - Course completion percentage
   - Module completion status
   - Estimated time to completion

### Advanced Metrics (Intermediate & Advanced Tiers)

7. **Time Analytics**
   - Time spent per course
   - Time spent per module
   - Time spent per day/week
   - Learning velocity (modules/week)

8. **Performance Analytics**
   - Quiz performance trends
   - Lab score progression
   - Weak areas identification
   - Strength areas identification

### Detailed Analytics (Advanced Tier Only)

9. **Learning Patterns**
   - **Heatmap**: Calendar view of daily activity
   - **Time Series**: Learning trends over time
   - **Comparative Analytics**: Anonymous peer benchmarking
   - **Predictive Insights**: Estimated completion dates
   - **Engagement Score**: Overall learning engagement metric

---

## Progress Data Schema

### User Progress Document

```json
{
  "user_id": "user_12345",
  "email": "student@example.com",
  "tier": "intermediate",
  "enrolled_courses": [
    {
      "course_id": "ai-03-nlp-transformers",
      "course_title": "Natural Language Processing with Transformers",
      "enrollment_date": "2026-01-01T00:00:00Z",
      "last_accessed": "2026-01-14T10:30:00Z",
      "overall_progress": 67,
      "status": "in_progress",
      "estimated_completion": "2026-02-15",
      
      "modules": [
        {
          "module_id": "module-01",
          "module_title": "Introduction to NLP",
          "progress": 100,
          "status": "completed",
          "started_at": "2026-01-01T10:00:00Z",
          "completed_at": "2026-01-05T15:30:00Z",
          "time_spent_seconds": 14400,
          
          "videos": [
            {
              "video_id": "v01",
              "video_title": "What is NLP?",
              "watched": true,
              "completion_percentage": 100,
              "time_watched_seconds": 1200,
              "last_position_seconds": 1200,
              "started_at": "2026-01-01T10:00:00Z",
              "completed_at": "2026-01-01T10:20:00Z"
            },
            {
              "video_id": "v02",
              "video_title": "Text Preprocessing",
              "watched": true,
              "completion_percentage": 100,
              "time_watched_seconds": 1500,
              "last_position_seconds": 1500,
              "started_at": "2026-01-02T11:00:00Z",
              "completed_at": "2026-01-02T11:25:00Z"
            }
          ],
          
          "slides": [
            {
              "slide_deck_id": "slides-01",
              "slide_deck_title": "NLP Fundamentals",
              "viewed": true,
              "slides_count": 45,
              "slides_viewed": 45,
              "time_spent_seconds": 1800,
              "last_viewed": "2026-01-03T14:00:00Z"
            }
          ],
          
          "labs": [
            {
              "lab_id": "lab-01",
              "lab_title": "Tokenization Practice",
              "status": "completed",
              "score": 95,
              "max_score": 100,
              "attempts": 2,
              "time_spent_seconds": 3600,
              "started_at": "2026-01-04T09:00:00Z",
              "completed_at": "2026-01-04T10:00:00Z",
              "best_score": 95
            }
          ],
          
          "quiz": {
            "quiz_id": "quiz-01",
            "quiz_title": "NLP Basics Quiz",
            "status": "completed",
            "score": 8,
            "max_score": 10,
            "percentage": 80,
            "attempts": 2,
            "best_score": 8,
            "last_attempt": "2026-01-05T15:00:00Z",
            "passed": true,
            "passing_score": 70
          }
        },
        
        {
          "module_id": "module-02",
          "module_title": "Word Embeddings",
          "progress": 60,
          "status": "in_progress",
          "started_at": "2026-01-06T10:00:00Z",
          "time_spent_seconds": 7200,
          
          "videos": [
            {
              "video_id": "v03",
              "video_title": "Introduction to Word2Vec",
              "watched": true,
              "completion_percentage": 100,
              "time_watched_seconds": 1400,
              "last_position_seconds": 1400,
              "started_at": "2026-01-06T10:00:00Z",
              "completed_at": "2026-01-06T10:23:00Z"
            },
            {
              "video_id": "v04",
              "video_title": "GloVe Embeddings",
              "watched": false,
              "completion_percentage": 45,
              "time_watched_seconds": 540,
              "last_position_seconds": 540,
              "started_at": "2026-01-07T11:00:00Z"
            }
          ],
          
          "slides": [
            {
              "slide_deck_id": "slides-02",
              "slide_deck_title": "Word Embeddings Deep Dive",
              "viewed": true,
              "slides_count": 52,
              "slides_viewed": 30,
              "time_spent_seconds": 1200,
              "last_viewed": "2026-01-07T14:00:00Z"
            }
          ],
          
          "labs": [
            {
              "lab_id": "lab-02",
              "lab_title": "Build Word2Vec Model",
              "status": "not_started",
              "attempts": 0
            }
          ],
          
          "quiz": {
            "quiz_id": "quiz-02",
            "quiz_title": "Word Embeddings Quiz",
            "status": "not_started",
            "attempts": 0
          }
        }
      ],
      
      "overall_stats": {
        "total_modules": 8,
        "completed_modules": 1,
        "videos_watched": 3,
        "total_videos": 24,
        "labs_completed": 1,
        "total_labs": 8,
        "quizzes_passed": 1,
        "total_quizzes": 8,
        "total_time_spent_seconds": 21600,
        "average_quiz_score": 80,
        "average_lab_score": 95
      },
      
      "certificates_earned": [
        {
          "certificate_id": "cert-ai-03-nlp-2026-01-15",
          "course_id": "ai-03-nlp-transformers",
          "issued_date": "2026-01-15T12:00:00Z",
          "final_score": 92,
          "blockchain_verified": false,
          "verification_url": "https://verify.gai-observe.com/cert-ai-03-nlp-2026-01-15"
        }
      ]
    }
  ],
  
  "global_stats": {
    "total_courses_enrolled": 3,
    "total_courses_completed": 0,
    "total_learning_time_hours": 87,
    "total_videos_watched": 45,
    "total_labs_completed": 12,
    "total_quizzes_passed": 10,
    "total_certificates": 0,
    "member_since": "2025-12-15T00:00:00Z",
    "last_active": "2026-01-14T10:30:00Z",
    "current_streak_days": 7,
    "longest_streak_days": 15
  }
}
```

---

## Progress Calculation Logic

### Course Completion Percentage

```python
def calculate_course_progress(course_data: dict) -> float:
    """
    Calculate overall course completion percentage
    
    Weights:
    - Videos: 40%
    - Quizzes: 30%
    - Labs: 20%
    - Slides: 10%
    """
    
    weights = {
        'videos': 0.40,
        'quizzes': 0.30,
        'labs': 0.20,
        'slides': 0.10
    }
    
    # Calculate component completion
    video_completion = calculate_video_completion(course_data['modules'])
    quiz_completion = calculate_quiz_completion(course_data['modules'])
    lab_completion = calculate_lab_completion(course_data['modules'])
    slide_completion = calculate_slide_completion(course_data['modules'])
    
    # Weighted average
    overall = (
        video_completion * weights['videos'] +
        quiz_completion * weights['quizzes'] +
        lab_completion * weights['labs'] +
        slide_completion * weights['slides']
    )
    
    return round(overall, 2)


def calculate_video_completion(modules: list) -> float:
    """Calculate video completion percentage"""
    total_videos = 0
    completed_videos = 0
    
    for module in modules:
        for video in module.get('videos', []):
            total_videos += 1
            if video['completion_percentage'] >= 95:
                completed_videos += 1
    
    return (completed_videos / total_videos * 100) if total_videos > 0 else 0


def calculate_quiz_completion(modules: list) -> float:
    """Calculate quiz completion percentage"""
    total_quizzes = 0
    passed_quizzes = 0
    
    for module in modules:
        quiz = module.get('quiz')
        if quiz and quiz['status'] != 'not_started':
            total_quizzes += 1
            if quiz.get('passed', False):
                passed_quizzes += 1
    
    return (passed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0


def calculate_lab_completion(modules: list) -> float:
    """Calculate lab completion percentage"""
    total_labs = 0
    completed_labs = 0
    
    for module in modules:
        for lab in module.get('labs', []):
            total_labs += 1
            if lab['status'] == 'completed':
                completed_labs += 1
    
    return (completed_labs / total_labs * 100) if total_labs > 0 else 0


def calculate_slide_completion(modules: list) -> float:
    """Calculate slide viewing completion"""
    total_slides = 0
    viewed_slides = 0
    
    for module in modules:
        for slide_deck in module.get('slides', []):
            total_slides += slide_deck['slides_count']
            viewed_slides += slide_deck['slides_viewed']
    
    return (viewed_slides / total_slides * 100) if total_slides > 0 else 0
```

---

## Progress Tracking UI Components

### Dashboard Overview

```python
# pages/1_🏠_Dashboard.py
import streamlit as st
import plotly.graph_objects as go
from utils.progress import get_user_progress

st.title("🏠 Dashboard")

# Get progress data
progress = get_user_progress(st.session_state['user_id'])

# Welcome message
st.subheader(f"Welcome back, {st.session_state['email'].split('@')[0].title()}!")

# Quick stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Courses In Progress",
        len([c for c in progress['enrolled_courses'] if c['status'] == 'in_progress'])
    )

with col2:
    st.metric(
        "Overall Completion",
        f"{progress['global_stats']['total_courses_completed']}/{progress['global_stats']['total_courses_enrolled']}"
    )

with col3:
    st.metric(
        "Certificates Earned",
        progress['global_stats']['total_certificates']
    )

with col4:
    st.metric(
        "Current Streak",
        f"{progress['global_stats']['current_streak_days']} days",
        delta=f"Best: {progress['global_stats']['longest_streak_days']}"
    )

# Continue Learning
st.markdown("---")
st.subheader("📚 Continue Learning")

recent_course = get_most_recent_course(progress)
if recent_course:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write(f"**{recent_course['course_title']}**")
        st.progress(recent_course['overall_progress'] / 100)
        st.caption(f"{recent_course['overall_progress']}% complete")
    
    with col2:
        if st.button("Resume", type="primary"):
            st.session_state['current_course_id'] = recent_course['course_id']
            st.switch_page("pages/3_🎓_Course_Player.py")
```

### Detailed Progress Page

```python
# pages/5_📊_My_Progress.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.progress import get_user_progress, get_tier_config

st.title("📊 My Progress")

# Get data
progress = get_user_progress(st.session_state['user_id'])
tier = st.session_state['tier'].lower()
config = get_tier_config(tier)

# Tier-appropriate analytics
analytics_level = config['analytics_level']

# Course selector
courses = progress['enrolled_courses']
selected_course = st.selectbox(
    "Select Course",
    options=courses,
    format_func=lambda c: c['course_title']
)

# Course progress overview
st.subheader(f"{selected_course['course_title']}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Overall Progress", f"{selected_course['overall_progress']}%")

with col2:
    st.metric(
        "Modules Completed",
        f"{selected_course['overall_stats']['completed_modules']}/{selected_course['overall_stats']['total_modules']}"
    )

with col3:
    hours = selected_course['overall_stats']['total_time_spent_seconds'] / 3600
    st.metric("Time Spent", f"{hours:.1f} hours")

# Module breakdown
st.markdown("---")
st.subheader("Module Progress")

for module in selected_course['modules']:
    with st.expander(f"{module['module_title']} - {module['progress']}%"):
        st.progress(module['progress'] / 100)
        
        # Module details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            video_count = len([v for v in module['videos'] if v['watched']])
            st.write(f"**Videos:** {video_count}/{len(module['videos'])}")
        
        with col2:
            if module.get('quiz') and module['quiz']['status'] != 'not_started':
                st.write(f"**Quiz:** {module['quiz']['score']}/{module['quiz']['max_score']}")
        
        with col3:
            lab_count = len([l for l in module['labs'] if l['status'] == 'completed'])
            st.write(f"**Labs:** {lab_count}/{len(module['labs'])}")

# Visualizations (tier-dependent)
if analytics_level in ['advanced', 'detailed']:
    st.markdown("---")
    st.subheader("📈 Performance Analytics")
    
    # Quiz scores trend
    quiz_scores = extract_quiz_scores(selected_course)
    if quiz_scores:
        fig = px.line(
            quiz_scores,
            x='module',
            y='score',
            title='Quiz Performance Trend',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Lab scores
    lab_scores = extract_lab_scores(selected_course)
    if lab_scores:
        fig = px.bar(
            lab_scores,
            x='lab',
            y='score',
            title='Lab Scores',
            color='score',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)

# Heatmap (Advanced tier only)
if config.get('analytics_heatmap'):
    st.markdown("---")
    st.subheader("🔥 Learning Activity Heatmap")
    
    heatmap_data = generate_activity_heatmap(progress)
    render_calendar_heatmap(heatmap_data)

# Export analytics (Advanced tier only)
if config.get('analytics_export'):
    st.markdown("---")
    
    if st.button("📥 Export Progress Report (CSV)"):
        csv_data = generate_progress_csv(selected_course)
        st.download_button(
            "Download CSV",
            data=csv_data,
            file_name=f"progress_{selected_course['course_id']}.csv",
            mime="text/csv"
        )
```

### Calendar Heatmap (Advanced Tier)

```python
def render_calendar_heatmap(activity_data: dict):
    """Render GitHub-style activity heatmap"""
    
    import plotly.graph_objects as go
    import pandas as pd
    from datetime import datetime, timedelta
    
    # Prepare data
    dates = []
    values = []
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        dates.append(date_str)
        values.append(activity_data.get(date_str, 0))
        current_date += timedelta(days=1)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=[values],
        x=dates,
        colorscale='Greens',
        showscale=True,
        hovertemplate='Date: %{x}<br>Minutes: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Daily Learning Activity (Past Year)",
        xaxis_title="Date",
        height=200
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

---

## Progress Synchronization

### Real-Time Updates

```python
# utils/progress_sync.py
import requests

def sync_video_progress(user_id: str, video_id: str, position: float, duration: float):
    """Sync video progress to backend"""
    
    completion = (position / duration * 100) if duration > 0 else 0
    
    payload = {
        'user_id': user_id,
        'video_id': video_id,
        'position_seconds': position,
        'completion_percentage': completion,
        'watched': completion >= 95,
        'timestamp': datetime.now().isoformat()
    }
    
    response = requests.post(
        f"{API_URL}/api/v1/progress/video",
        json=payload,
        headers={'Authorization': f"Bearer {st.session_state['token']}"}
    )
    
    return response.status_code == 200


def sync_quiz_completion(user_id: str, quiz_id: str, score: int, max_score: int):
    """Sync quiz completion"""
    
    payload = {
        'user_id': user_id,
        'quiz_id': quiz_id,
        'score': score,
        'max_score': max_score,
        'percentage': (score / max_score * 100),
        'passed': (score / max_score) >= 0.7,
        'timestamp': datetime.now().isoformat()
    }
    
    response = requests.post(
        f"{API_URL}/api/v1/progress/quiz",
        json=payload,
        headers={'Authorization': f"Bearer {st.session_state['token']}"}
    )
    
    return response.status_code == 200


def sync_lab_completion(user_id: str, lab_id: str, score: int, time_spent: int):
    """Sync lab completion (called by SimulationPlayer webhook)"""
    
    payload = {
        'user_id': user_id,
        'lab_id': lab_id,
        'score': score,
        'status': 'completed',
        'time_spent_seconds': time_spent,
        'timestamp': datetime.now().isoformat()
    }
    
    response = requests.post(
        f"{API_URL}/api/v1/progress/lab",
        json=payload,
        headers={'Authorization': f"Bearer {st.session_state['token']}"}
    )
    
    return response.status_code == 200
```

---

## Achievement Badges

### Badge System

```python
BADGES = {
    'first_video': {
        'name': 'First Steps',
        'description': 'Watched your first video',
        'icon': '🎬'
    },
    'module_complete': {
        'name': 'Module Master',
        'description': 'Completed your first module',
        'icon': '📘'
    },
    'perfect_quiz': {
        'name': 'Perfect Score',
        'description': 'Scored 100% on a quiz',
        'icon': '💯'
    },
    'lab_expert': {
        'name': 'Lab Expert',
        'description': 'Completed 10 labs',
        'icon': '🧪'
    },
    'week_streak': {
        'name': '7-Day Streak',
        'description': 'Learned for 7 consecutive days',
        'icon': '🔥'
    },
    'course_complete': {
        'name': 'Course Champion',
        'description': 'Completed your first course',
        'icon': '🏆'
    }
}

def check_and_award_badges(user_id: str, progress_data: dict):
    """Check if user earned new badges"""
    
    newly_earned = []
    
    # Check each badge condition
    if progress_data['global_stats']['total_videos_watched'] == 1:
        newly_earned.append('first_video')
    
    if progress_data['global_stats']['current_streak_days'] >= 7:
        newly_earned.append('week_streak')
    
    # Award badges
    for badge_id in newly_earned:
        award_badge(user_id, badge_id)
        st.balloons()
        st.success(f"🎉 Badge Earned: {BADGES[badge_id]['icon']} {BADGES[badge_id]['name']}")
```

---

## Testing

### Progress Calculation Tests

```python
def test_course_progress_calculation():
    course_data = {
        'modules': [
            {
                'videos': [
                    {'completion_percentage': 100},
                    {'completion_percentage': 50}
                ],
                'quiz': {'status': 'completed', 'passed': True},
                'labs': [{'status': 'completed'}],
                'slides': [{'slides_count': 10, 'slides_viewed': 10}]
            }
        ]
    }
    
    progress = calculate_course_progress(course_data)
    assert 0 <= progress <= 100
```

---

## Conclusion

The progress tracking system provides comprehensive monitoring of student learning activities with tier-appropriate detail levels. The implementation ensures accurate tracking, real-time synchronization, and insightful visualizations to keep students motivated and informed of their learning journey.

