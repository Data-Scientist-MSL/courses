# CoursePlayerApp Progress Tracking Specification

## Overview

The Progress Tracking system monitors student learning activities, provides visual feedback on achievements, and motivates continued engagement through gamification elements. All tiers receive basic progress tracking, with enhanced analytics for higher tiers.

---

## Progress Metrics

### Core Metrics (All Tiers)

#### 1. Videos Watched
- **Metric**: Number and percentage of videos completed
- **Completion Criteria**: Video is marked complete at 90% watched
- **Display**: 
  - Progress bar per module
  - Checkmarks on completed videos
  - "Resume watching" for in-progress videos

#### 2. Labs Completed
- **Metric**: Number of labs submitted and passed
- **Grading**: Auto-graded labs show score (0-100%)
- **Display**:
  - Lab status: Not Started, In Progress, Completed, Passed
  - Completion percentage per module

#### 3. Quizzes/Assessments Passed
- **Metric**: Quiz scores and pass/fail status
- **Pass Criteria**: Typically 70% or higher
- **Display**:
  - Score out of total points
  - Attempt history
  - Best score highlighted

#### 4. Simulations Completed
- **Metric**: Interactive simulation completion status
- **Data Tracked**: 
  - Completion percentage
  - Time spent
  - Score/performance
- **Display**: Badge or checkmark on completed simulations

#### 5. Study Time
- **Metric**: Total time spent learning
- **Granularity**: Per course, per module, per day/week/month
- **Tracking Method**: Active engagement time (video playing, code executing, quiz taking)
- **Display**: 
  - Total hours
  - Time breakdown by activity type
  - Time trend chart (Intermediate/Advanced)

#### 6. Current Streak
- **Metric**: Consecutive days with learning activity
- **Activity Definition**: At least 15 minutes of engagement per day
- **Display**:
  - Streak counter (e.g., "🔥 7-day streak")
  - Calendar heatmap (Intermediate/Advanced)
  - Longest streak record

#### 7. Overall Course Completion
- **Metric**: Percentage of course completed
- **Calculation**: Weighted average of videos, labs, quizzes, simulations
- **Weights**:
  ```python
  completion_percent = (
      0.40 * videos_completed_percent +
      0.30 * labs_completed_percent +
      0.20 * quizzes_completed_percent +
      0.10 * simulations_completed_percent
  )
  ```
- **Display**: 
  - Large progress bar on dashboard
  - Estimated time to completion

---

## Data Model

### Database Schema

```sql
-- Main progress tracking table
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    course_id VARCHAR(50) NOT NULL,
    module_id VARCHAR(50),
    resource_type VARCHAR(20) NOT NULL,  -- 'video', 'lab', 'quiz', 'simulation', 'reading'
    resource_id VARCHAR(100) NOT NULL,
    
    -- Progress data
    status VARCHAR(20) NOT NULL DEFAULT 'not_started',  -- 'not_started', 'in_progress', 'completed', 'passed', 'failed'
    completion_percent INT DEFAULT 0 CHECK (completion_percent >= 0 AND completion_percent <= 100),
    score INT,  -- For quizzes/labs (0-100)
    time_spent_seconds INT DEFAULT 0,
    
    -- Resume functionality
    last_position TEXT,  -- JSON for video timestamp, code state, etc.
    
    -- Timestamps
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Indexes
    UNIQUE(user_id, course_id, resource_type, resource_id),
    INDEX idx_user_course (user_id, course_id),
    INDEX idx_status (status),
    INDEX idx_completion (user_id, completed_at)
);

-- Daily activity tracking for streaks
CREATE TABLE daily_activity (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    activity_date DATE NOT NULL,
    time_spent_seconds INT DEFAULT 0,
    activities_completed INT DEFAULT 0,
    courses_accessed TEXT[],  -- Array of course IDs
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, activity_date),
    INDEX idx_user_date (user_id, activity_date)
);

-- Achievements/badges
CREATE TABLE user_achievements (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    achievement_type VARCHAR(50) NOT NULL,  -- 'first_video', 'streak_7', 'course_complete', etc.
    achievement_id VARCHAR(100) NOT NULL,
    metadata JSONB,  -- Additional data (course_id, score, etc.)
    
    earned_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, achievement_type, achievement_id),
    INDEX idx_user_achievements (user_id, earned_at)
);

-- Learning sessions (for detailed analytics)
CREATE TABLE learning_sessions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    course_id VARCHAR(50),
    
    session_start TIMESTAMP NOT NULL,
    session_end TIMESTAMP,
    duration_seconds INT,
    
    activities JSONB,  -- Array of {type, resource_id, duration} objects
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_sessions (user_id, session_start)
);
```

---

## Progress Tracking Implementation

### Progress Tracker Service

```python
# courseplayerapp/progress/tracker.py

from datetime import datetime, date, timedelta
from typing import Optional, Dict, List
import psycopg2

class ProgressTracker:
    """Track and retrieve user progress across courses."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.db = get_database_connection()
    
    def update_progress(
        self,
        course_id: str,
        module_id: str,
        resource_type: str,
        resource_id: str,
        completion_percent: int = 0,
        time_spent: int = 0,
        score: Optional[int] = None,
        last_position: Optional[str] = None
    ):
        """
        Update progress for a specific resource.
        
        Args:
            course_id: Course identifier
            module_id: Module identifier
            resource_type: Type of resource (video, lab, quiz, etc.)
            resource_id: Unique resource identifier
            completion_percent: Completion percentage (0-100)
            time_spent: Time spent in seconds
            score: Score if applicable (0-100)
            last_position: Resume position (JSON string)
        """
        # Determine status
        if completion_percent == 0:
            status = 'not_started'
        elif completion_percent >= 90:
            status = 'completed'
        else:
            status = 'in_progress'
        
        # If there's a score, determine pass/fail
        if score is not None:
            status = 'passed' if score >= 70 else 'failed'
        
        # Set timestamps
        started_at = datetime.now() if completion_percent > 0 else None
        completed_at = datetime.now() if status in ['completed', 'passed'] else None
        
        # Insert or update progress
        query = """
            INSERT INTO user_progress (
                user_id, course_id, module_id, resource_type, resource_id,
                status, completion_percent, score, time_spent_seconds,
                last_position, started_at, completed_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (user_id, course_id, resource_type, resource_id)
            DO UPDATE SET
                status = EXCLUDED.status,
                completion_percent = EXCLUDED.completion_percent,
                score = EXCLUDED.score,
                time_spent_seconds = user_progress.time_spent_seconds + EXCLUDED.time_spent_seconds,
                last_position = EXCLUDED.last_position,
                started_at = COALESCE(user_progress.started_at, EXCLUDED.started_at),
                completed_at = EXCLUDED.completed_at,
                updated_at = NOW()
        """
        
        self.db.execute(query, (
            self.user_id, course_id, module_id, resource_type, resource_id,
            status, completion_percent, score, time_spent,
            last_position, started_at, completed_at
        ))
        
        # Update daily activity
        self._update_daily_activity(course_id, time_spent)
        
        # Check for achievements
        if status in ['completed', 'passed']:
            self._check_achievements(course_id, resource_type, resource_id)
    
    def get_course_progress(self, course_id: str) -> Dict:
        """
        Get overall progress for a course.
        
        Returns:
            {
                "completion_percent": 73,
                "videos_completed": 15,
                "videos_total": 20,
                "labs_completed": 8,
                "labs_total": 10,
                "quizzes_passed": 5,
                "quizzes_total": 5,
                "time_spent_hours": 12.5,
                "current_module": "Module 3",
                "estimated_time_remaining_hours": 5
            }
        """
        # Get all progress for this course
        query = """
            SELECT 
                resource_type,
                COUNT(*) as total,
                SUM(CASE WHEN status IN ('completed', 'passed') THEN 1 ELSE 0 END) as completed,
                SUM(time_spent_seconds) as total_time
            FROM user_progress
            WHERE user_id = %s AND course_id = %s
            GROUP BY resource_type
        """
        
        results = self.db.query(query, (self.user_id, course_id))
        
        # Process results
        progress = {
            "videos_completed": 0,
            "videos_total": 0,
            "labs_completed": 0,
            "labs_total": 0,
            "quizzes_passed": 0,
            "quizzes_total": 0,
            "time_spent_hours": 0
        }
        
        total_time = 0
        for row in results:
            if row['resource_type'] == 'video':
                progress['videos_completed'] = row['completed']
                progress['videos_total'] = row['total']
            elif row['resource_type'] == 'lab':
                progress['labs_completed'] = row['completed']
                progress['labs_total'] = row['total']
            elif row['resource_type'] == 'quiz':
                progress['quizzes_passed'] = row['completed']
                progress['quizzes_total'] = row['total']
            
            total_time += row['total_time'] or 0
        
        progress['time_spent_hours'] = round(total_time / 3600, 1)
        
        # Calculate overall completion
        progress['completion_percent'] = self._calculate_overall_completion(
            progress['videos_completed'],
            progress['videos_total'],
            progress['labs_completed'],
            progress['labs_total'],
            progress['quizzes_passed'],
            progress['quizzes_total']
        )
        
        return progress
    
    def get_current_streak(self) -> Dict:
        """
        Get user's current learning streak.
        
        Returns:
            {
                "current_streak": 7,
                "longest_streak": 15,
                "last_activity_date": "2026-01-14"
            }
        """
        query = """
            SELECT activity_date, time_spent_seconds
            FROM daily_activity
            WHERE user_id = %s AND time_spent_seconds >= 900
            ORDER BY activity_date DESC
            LIMIT 100
        """
        
        activities = self.db.query(query, (self.user_id,))
        
        if not activities:
            return {"current_streak": 0, "longest_streak": 0, "last_activity_date": None}
        
        # Calculate current streak
        current_streak = 0
        expected_date = date.today()
        
        for activity in activities:
            if activity['activity_date'] == expected_date or \
               activity['activity_date'] == expected_date - timedelta(days=1):
                current_streak += 1
                expected_date = activity['activity_date'] - timedelta(days=1)
            else:
                break
        
        # Calculate longest streak (historical)
        longest_streak = self._calculate_longest_streak(activities)
        
        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "last_activity_date": activities[0]['activity_date'].isoformat() if activities else None
        }
    
    def _update_daily_activity(self, course_id: str, time_spent: int):
        """Update daily activity record."""
        today = date.today()
        
        query = """
            INSERT INTO daily_activity (user_id, activity_date, time_spent_seconds, activities_completed, courses_accessed)
            VALUES (%s, %s, %s, 1, ARRAY[%s])
            ON CONFLICT (user_id, activity_date)
            DO UPDATE SET
                time_spent_seconds = daily_activity.time_spent_seconds + EXCLUDED.time_spent_seconds,
                activities_completed = daily_activity.activities_completed + 1,
                courses_accessed = array_append(daily_activity.courses_accessed, %s),
                updated_at = NOW()
        """
        
        self.db.execute(query, (self.user_id, today, time_spent, course_id, course_id))
    
    def _calculate_overall_completion(
        self,
        videos_done: int,
        videos_total: int,
        labs_done: int,
        labs_total: int,
        quizzes_done: int,
        quizzes_total: int
    ) -> int:
        """Calculate weighted overall completion percentage."""
        if videos_total == 0 and labs_total == 0 and quizzes_total == 0:
            return 0
        
        video_pct = (videos_done / videos_total * 100) if videos_total > 0 else 0
        lab_pct = (labs_done / labs_total * 100) if labs_total > 0 else 0
        quiz_pct = (quizzes_done / quizzes_total * 100) if quizzes_total > 0 else 0
        
        overall = (0.4 * video_pct + 0.3 * lab_pct + 0.3 * quiz_pct)
        return int(overall)
    
    def _check_achievements(self, course_id: str, resource_type: str, resource_id: str):
        """Check if user earned any achievements."""
        # First video completed
        if resource_type == 'video':
            video_count = self.db.query_one(
                "SELECT COUNT(*) as count FROM user_progress WHERE user_id = %s AND resource_type = 'video' AND status = 'completed'",
                (self.user_id,)
            )
            if video_count['count'] == 1:
                self._award_achievement('first_video', 'global')
        
        # Check streak achievements
        streak_info = self.get_current_streak()
        if streak_info['current_streak'] == 7:
            self._award_achievement('streak_7', 'global')
        elif streak_info['current_streak'] == 30:
            self._award_achievement('streak_30', 'global')
        
        # Course completion
        progress = self.get_course_progress(course_id)
        if progress['completion_percent'] >= 100:
            self._award_achievement('course_complete', course_id)
    
    def _award_achievement(self, achievement_type: str, achievement_id: str):
        """Award an achievement to the user."""
        query = """
            INSERT INTO user_achievements (user_id, achievement_type, achievement_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, achievement_type, achievement_id) DO NOTHING
        """
        self.db.execute(query, (self.user_id, achievement_type, achievement_id))
    
    def _calculate_longest_streak(self, activities: List[Dict]) -> int:
        """Calculate longest historical streak."""
        if not activities:
            return 0
        
        longest = 1
        current = 1
        prev_date = activities[0]['activity_date']
        
        for activity in activities[1:]:
            if activity['activity_date'] == prev_date - timedelta(days=1):
                current += 1
                longest = max(longest, current)
            else:
                current = 1
            prev_date = activity['activity_date']
        
        return longest
```

---

## Achievements & Gamification

### Achievement Types

```python
ACHIEVEMENTS = {
    # First-time achievements
    "first_video": {
        "title": "First Steps",
        "description": "Watched your first video",
        "icon": "🎬",
        "points": 10
    },
    "first_lab": {
        "title": "Code Warrior",
        "description": "Completed your first lab",
        "icon": "💻",
        "points": 20
    },
    "first_quiz": {
        "title": "Quiz Master",
        "description": "Passed your first quiz",
        "icon": "✅",
        "points": 15
    },
    
    # Streak achievements
    "streak_7": {
        "title": "Week Warrior",
        "description": "7-day learning streak",
        "icon": "🔥",
        "points": 50
    },
    "streak_30": {
        "title": "Monthly Master",
        "description": "30-day learning streak",
        "icon": "🏆",
        "points": 200
    },
    "streak_100": {
        "title": "Century Club",
        "description": "100-day learning streak",
        "icon": "💎",
        "points": 1000
    },
    
    # Course completion
    "course_complete": {
        "title": "Course Champion",
        "description": "Completed a full course",
        "icon": "🎓",
        "points": 500
    },
    
    # Speed achievements
    "speed_learner": {
        "title": "Speed Learner",
        "description": "Completed course in under 30 days",
        "icon": "⚡",
        "points": 300
    },
    
    # Perfect scores
    "perfect_quiz": {
        "title": "Perfect Score",
        "description": "Got 100% on a quiz",
        "icon": "⭐",
        "points": 100
    },
    
    # Social achievements
    "helpful_peer": {
        "title": "Helpful Peer",
        "description": "Answered 10 forum questions",
        "icon": "🤝",
        "points": 150
    }
}
```

### Leaderboard (Optional, Privacy-Respecting)

```python
# courseplayerapp/progress/leaderboard.py

class Leaderboard:
    """Anonymous leaderboard for course progress (Advanced tier only)."""
    
    def get_course_leaderboard(
        self,
        course_id: str,
        limit: int = 10,
        anonymous: bool = True
    ) -> List[Dict]:
        """
        Get top learners in a course.
        
        Args:
            course_id: Course to get leaderboard for
            limit: Number of top learners to return
            anonymous: If True, hide user names (show as "User #123")
        
        Returns:
            List of {rank, user_id/name, completion_percent, time_spent}
        """
        query = """
            SELECT 
                user_id,
                MAX(completion_percent) as completion,
                SUM(time_spent_seconds) as total_time,
                ROW_NUMBER() OVER (ORDER BY MAX(completion_percent) DESC, SUM(time_spent_seconds) ASC) as rank
            FROM user_progress
            WHERE course_id = %s
            GROUP BY user_id
            ORDER BY completion DESC, total_time ASC
            LIMIT %s
        """
        
        results = self.db.query(query, (course_id, limit))
        
        leaderboard = []
        for row in results:
            entry = {
                "rank": row['rank'],
                "completion_percent": row['completion'],
                "time_spent_hours": round(row['total_time'] / 3600, 1)
            }
            
            if anonymous:
                entry["name"] = f"User #{row['user_id'] % 10000}"
            else:
                user = get_user(row['user_id'])
                entry["name"] = user['name']
            
            leaderboard.append(entry)
        
        return leaderboard
```

---

## Progress Visualization

### UI Components (Streamlit)

```python
# courseplayerapp/ui/components/progress_tracker.py

import streamlit as st
import pandas as pd
import plotly.express as px
from courseplayerapp.progress.tracker import ProgressTracker

def render_progress_dashboard(course_id: str, user_tier: str):
    """Render progress dashboard for a course."""
    
    tracker = ProgressTracker(st.session_state.user_id)
    progress = tracker.get_course_progress(course_id)
    streak = tracker.get_current_streak()
    
    st.header("Your Progress")
    
    # Overall completion
    st.subheader("Course Completion")
    st.progress(progress['completion_percent'] / 100)
    st.caption(f"{progress['completion_percent']}% complete")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Videos Watched",
            f"{progress['videos_completed']}/{progress['videos_total']}",
            f"{int(progress['videos_completed']/progress['videos_total']*100)}%"
        )
    
    with col2:
        st.metric(
            "Labs Completed",
            f"{progress['labs_completed']}/{progress['labs_total']}",
            f"{int(progress['labs_completed']/progress['labs_total']*100) if progress['labs_total'] > 0 else 0}%"
        )
    
    with col3:
        st.metric(
            "Study Time",
            f"{progress['time_spent_hours']} hrs"
        )
    
    with col4:
        st.metric(
            "Current Streak",
            f"{streak['current_streak']} days",
            delta=f"Record: {streak['longest_streak']}"
        )
    
    # Detailed analytics (Intermediate/Advanced tiers only)
    if user_tier in ["intermediate", "advanced"]:
        st.subheader("Detailed Analytics")
        
        # Time spent breakdown (would need more data from DB)
        st.caption("⚡ Available in Intermediate and Advanced tiers")
        
        # Example chart placeholder
        chart_data = pd.DataFrame({
            "Activity": ["Videos", "Labs", "Quizzes"],
            "Hours": [5.2, 3.8, 1.5]
        })
        
        fig = px.pie(chart_data, values="Hours", names="Activity", title="Time Breakdown")
        st.plotly_chart(fig)
    else:
        st.info("💎 Upgrade to Intermediate or Advanced for detailed analytics and insights")
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-14  
**Author**: EdGuide Progress Team  
**Platform**: EdGuide (gai-observe.online)
